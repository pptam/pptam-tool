class ExptsController < ApplicationController
  before_filter :get_expt, :except => [:index, :new, :new_from_compare, :create, :las, :lac]
  around_filter :respond_catch_exception_rjs, :only => [:create, :new_from_compare, :show_section, :custom_query]
  # GET /expts
  def index
    @expts = user_session.get_expts
  end

  # GET /expts/1
  def show
    @tool = params[:tool]
    if @tool.nil? then
      @tool = default_tool_for(@expt)
    elsif !@expt.tools.keys.find {|t| t == @tool}
      flash[:error] = "Could not find tool #{@tool.inspect}"
    end
    @expt.execute_sections_for_tool(@tool)  
  end

  def view
    if params[:sectionid] then
      @section = @expt.find_section_with_id(params[:sectionid])
      raise "Section not found" unless @section
      @section.execute(@expt.db) unless @section.executed?
    end
  end

  def show_section
    @section = @expt.find_section_with_id(params[:sectionid])
    raise "Section with id #{params[:sectionid]} not found" unless @section
    @section.execute(@expt.db) unless @section.executed?
    respond_to do |format|
      format.js { render :action => 'show_section.rjs', :locals =>{ :section => @section }}
    end
  end

  # GET /expts/new
  def new
    @expt = Expt.new
  end

  # POST /expts
  def create
    @expt = Expt.new(params[:expt])
    @expts = user_session.get_expts
    if user_session.loaded?(@expt.to_param) then
      raise "Experiment is already loaded"
    end
    @expt.load_from_disk
    user_session.save_expt(@expt)
    if params[:show] then
      redirect_to expt_url @expt and return
    end
    @expts = user_session.get_expts
    respond_to do |format|
      format.js { render :action => 'new.rjs'}
    end
  end

  def las #load and show
    load(params[:expt])
    redirect_to expt_url @expt
  end

  def lac #load and compare
    @expts = user_session.get_expts
    if params[:expts].nil? or params[:expts].length < 2
      raise "You need to select atleast two experiments to compare"
    end    
    cexpts = params[:expts].collect {|e| load({:path=>e})}
    name = "Compare_" + cexpts.collect{|e| e.name}.join("_")
    @expt = Expt.new({:path=>name})
    unless user_session.loaded?(@expt.to_param) then
      @expt.compare_loaded_databases(cexpts)
      @expt.name = name
      user_session.save_expt(@expt)
    end
    redirect_to expt_url @expt and return
  end

  # DELETE /expts/1
  def destroy
    user_session.delete_expt(params[:id])
    @expts = user_session.get_expts
    #@expt.destroy

    respond_to do |format|
      format.js { render :action => 'delete.rjs'}
    end
  end

  def image
    section = @expt.find_section_with_id(params[:sectionid])
    send_data(section.image,
      :disposition => 'inline',
      :type => 'image/png',
      :filename => section.desc.gsub(/ /,"")+".png")
  end

  def sparkline
    section = @expt.find_section_with_id(params[:sectionid])
    data = section.sparkline(params[:i].to_i, params[:j].to_i)
    send_data(data,
      :disposition => 'inline',
      :type => 'image/png',
      :filename => section.desc.gsub(/ /,"")+".png")
  end

  def new_from_compare
    @expts = user_session.get_expts
    if params[:expts].nil? or params[:expts].length < 2
      raise "You need to select atleast two experiments to compare"
    end
    cexpts = params[:expts].collect {|e| user_session.find_expt(e)}
    name = "Compare_" + cexpts.collect{|e| e.name}.join("_")
    @expt = Expt.new({:path=>name})
    if user_session.loaded?(@expt.to_param) then
      raise "Experiment #{@expt.name}is already compared"
    end
    @expt.compare_loaded_databases(cexpts)
    @expt.name = name
    user_session.save_expt(@expt)
    @expts = user_session.get_expts
    respond_to do |format|
      format.js { render :action => 'new.rjs'}
    end
  end

  def custom_query
    desc = params[:desc]
    query = params[:query]
    dims = params[:dims]
    display = params[:display]
    @section = Fenxi.new_section(["Dynamic", desc, display, dims, query])
    @section.execute(@expt.db)
    @expt.tools["Dynamic"] << @section
    respond_to do |format|
      format.js { render :action => 'show_section.rjs', :locals =>{ :section => @section }}
    end
  end
  
  private
  # Ensure the experiment is loaded
  def load(phash)
    @expt = Expt.new(phash)
    logger.warn("Loading #{phash.inspect}")
    unless user_session.loaded?(@expt.to_param) then
      @expt.load_from_disk
      user_session.save_expt(@expt)
    end
    @expt
  end

  def get_expt
    @expt = user_session.find_expt(params[:id])
    @expts = user_session.get_expts
  end
  def default_tool_for(expt)
    #first search for profile, if not return 1st tool
    tool = expt.tools.keys.find {|name| name == "profile"}
    return tool unless tool.nil?
    return expt.tools.keys.first
  end
  def respond_catch_exception_rjs
    begin
      yield
    rescue Exception => ex
      logger.warn(ex.message)
      logger.warn(ex.backtrace[0..3].join("\n"))
      respond_to do |format|
        format.js do
          @error = ex.message # FIXME: Need a better way to do this
          render :action => 'error.rjs'
        end
      end
    end
  end
end
