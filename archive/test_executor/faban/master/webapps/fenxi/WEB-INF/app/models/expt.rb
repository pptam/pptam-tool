require 'fenxi'
class Expt < Fenxi::FenxiDatabase

  def to_param
    @path.gsub(/[\/\.]/,'_').downcase
  end
end
