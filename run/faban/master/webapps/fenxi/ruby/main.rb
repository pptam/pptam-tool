$LOAD_PATH << File.expand_path(File.dirname(__FILE__))
require 'fenxi'
f = case
when ARGV[0] == "view" then Fenxi::FenxiView.new(ARGV[1], ARGV[2],nil)
else Fenxi::FenxiCompare.new(ARGV[1..-1])
end
f.execute

unless ENV["FENXI_CSS_LOC"] then
  dest_dir = ARGV[0] == "view" ? ARGV[2] : ARGV[-1]
  %W|fenxi.css fenxi.js FenXi.jpg|.each do |file|
    FileUtils.install(ENV["FENXI_HOME"] + "/html/#{file}", dest_dir, :mode=> 0744)
  end
end
