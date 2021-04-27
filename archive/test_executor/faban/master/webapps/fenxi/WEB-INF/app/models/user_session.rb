class UserSession
  def initialize(session)
    @store = session
    @store[:expts] ||= []
    @store[:compare] ||= []
  end

  def save(tag, value)
    @store[tag] << value
  end

  def find(tag, param)
    @store[tag].detect { |l| l.to_param == param } || raise("#{param} not found")
  end

  def get(tag)
    @store[tag]
  end
  
  def save_expt(expt)
    save(:expts, expt)
  end

  def find_expt(param)
    find(:expts, param)
  end
  
  def loaded?(param)
    @store[:expts].detect { |l| l.to_param == param }
  end
  
  def delete_expt(param)
    @store[:expts].delete_if { |l| l.to_param == param }
  end
  
  def get_expts
    get(:expts)
  end

  def get_compare
    get(:compare)
  end

  def save_compare(comp)
    save(:compare, comp)
  end

  def find_compare(param)
    find(:compare, param)
  end

  def num_expts
    @store[:expts].length
  end
end
