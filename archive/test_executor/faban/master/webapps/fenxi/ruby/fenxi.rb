$LOAD_PATH << File.expand_path(File.dirname(__FILE__))

include Java
require 'erb'
require 'pp'
require 'fileutils'
require 'fenxi/database'
require 'fenxi/fenxi_database'
require 'fenxi/chart'
require 'fenxi/section'
require 'fenxi/fenxi_util'
require 'fenxi/fenxi_view'
require 'fenxi/merge_util'
require 'fenxi/fenxi_compare'
require 'fenxi/query_result'

