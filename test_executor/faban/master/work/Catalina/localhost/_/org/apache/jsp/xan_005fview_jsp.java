package org.apache.jsp;

import javax.servlet.*;
import javax.servlet.http.*;
import javax.servlet.jsp.*;
import com.sun.faban.harness.webclient.View;
import java.util.StringTokenizer;
import java.io.File;
import java.io.*;
import java.util.Set;
import java.util.*;
import java.net.URLEncoder;
import java.text.*;
import com.sun.faban.harness.common.Config;

public final class xan_005fview_jsp extends org.apache.jasper.runtime.HttpJspBase
    implements org.apache.jasper.runtime.JspSourceDependent {

  private static java.util.Vector _jspx_dependants;

  public java.util.List getDependants() {
    return _jspx_dependants;
  }

  public void _jspService(HttpServletRequest request, HttpServletResponse response)
        throws java.io.IOException, ServletException {

    JspFactory _jspxFactory = null;
    PageContext pageContext = null;
    HttpSession session = null;
    ServletContext application = null;
    ServletConfig config = null;
    JspWriter out = null;
    Object page = this;
    JspWriter _jspx_out = null;
    PageContext _jspx_page_context = null;


    try {
      _jspxFactory = JspFactory.getDefaultFactory();
      response.setContentType("text/html");
      pageContext = _jspxFactory.getPageContext(this, request, response,
      			null, true, 8192, true);
      _jspx_page_context = pageContext;
      application = pageContext.getServletContext();
      config = pageContext.getServletConfig();
      session = pageContext.getSession();
      out = pageContext.getOut();
      _jspx_out = out;

      out.write("<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.01//EN\">\n");
      out.write('\n');
      out.write('\n');

    response.setHeader("Cache-Control", "no-cache");
    View.Xan xan = (View.Xan)request.getAttribute("model");
    Boolean tblOnly = (Boolean)request.getAttribute("tblOnly");
    if (tblOnly == null)
        tblOnly = false;
    String[] rowClasses = {"even", "odd"};

      out.write("\n");
      out.write("\n");
      out.write("<html>\n");
      out.write("  <head>\n");
      out.write("    <meta http-equiv=\"Content-Type\" content=\"text/html; charset=UTF-8\">\n");
      out.write("    <title>");
      out.print( xan.title );
      out.write("</title>\n");
      out.write("    <link rel=\"icon\" type=\"image/gif\" href=\"/img/faban.gif\"/>\n");
      out.write("    <link rel=\"stylesheet\" type=\"text/css\" href=\"/css/style.css\" />\n");
      out.write("    <link rel=\"stylesheet\" type=\"text/css\" href=\"/css/xanview.css\"/>\n");
      out.write("    <!--[if lt IE 9]><script language=\"javascript\" type=\"text/javascript\" src=\"/scripts/excanvas.min.js\"></script>><![endif]-->\n");
      out.write("    <script language=\"javascript\" type=\"text/javascript\" src=\"/scripts/jquery.min.js\"></script>\n");
      out.write("    <script language=\"javascript\" type=\"text/javascript\" src=\"/scripts/jquery.jqplot.min.js\"></script>\n");
      out.write("    <script type=\"text/javascript\" src=\"/scripts/jqplot.cursor.min.js\"></script>\n");
      out.write("    <script type=\"text/javascript\" src=\"/scripts/jqplot.highlighter.min.js\"></script>\n");
      out.write("    <script language=\"javascript\" type=\"text/javascript\" src=\"/scripts/jqplot.canvasTextRenderer.min.js\"></script>\n");
      out.write("    <script language=\"javascript\" type=\"text/javascript\" src=\"/scripts/jqplot.canvasAxisLabelRenderer.min.js\"></script>\n");
      out.write("\n");
      out.write("    <script language=\"javascript\" type=\"text/javascript\" src=\"/scripts/jqplot.dateAxisRenderer.min.js\"></script>\n");
      out.write("    <link rel=\"stylesheet\" type=\"text/css\" href=\"/css/jquery.jqplot.css\" />\n");
      out.write("    <style>\n");
      out.write("\n");
      out.write("    .message {\n");
      out.write("        padding-left: 50px;\n");
      out.write("        font-size: smaller;\n");
      out.write("    }\n");
      out.write("    </style>\n");
      out.write("  </head>\n");
      out.write("  <body>\n");
      out.write("    <h1 class=\"page_title\" align=\"center\">");
      out.print( xan.title );
      out.write("</h1>\n");
      out.write("    <div id=\"toc\">\n");
      out.write("    <h2><a name=\"top\"></a>Contents</h2>\n");
      out.write("    <ul>\n");
      out.write("        ");
 for (int id = 0; id < xan.sections.size(); id++) {
            View.Section section = xan.sections.get(id);
        
      out.write("\n");
      out.write("        <li><a href=\"#");
      out.print( id );
      out.write('"');
      out.write('>');
      out.print( section.name );
      out.write("</a></li>\n");
      out.write("        ");
 } 
      out.write("\n");
      out.write("    </ul>\n");
      out.write("    </div>\n");
      out.write("    <br/>\n");
      out.write("    ");
 for (int id = 0; id < xan.sections.size(); id++) {
        View.Section section = xan.sections.get(id);
        if (section.link != null){ //link
        
      out.write("\n");
      out.write("            <h2><a name=\"");
      out.print( id );
      out.write("\" href=\"");
      out.print( section.link );
      out.write('"');
      out.write('>');
      out.print( section.name );
      out.write("</a></h2>\n");
      out.write("     ");
 } else {
      out.write("\n");
      out.write("            <h2><a name=\"");
      out.print( id );
      out.write("\"></a>");
      out.print( section.name );
      out.write("</h2>\n");
      out.write("    ");
 }
       if ("line".equalsIgnoreCase(section.display)) {
    
      out.write("\n");
      out.write("        <div id=\"graph");
      out.print( id );
      out.write("\" style=\"width: 600px; height: 300px; position: relative;\">\n");
      out.write("        </div>\n");
      out.write("    ");
 } else { 
      out.write("\n");
      out.write("    <table BORDER=0 CELLPADDING=4 CELLSPACING=3 style=\"padding:2px; border: 2px solid #cccccc;\">\n");
      out.write("        <tr>\n");
      out.write("        ");
 if (section.headers != null) {
                for (String header : section.headers) { 
      out.write("\n");
      out.write("                    <th class=\"header\">");
      out.print( header );
      out.write("</th>\n");
      out.write("             ");
 }
           } 
      out.write("\n");
      out.write("        </tr>\n");
      out.write("        ");
 for (int i = 0; i < section.rows.size(); i++) {
               List<String> row = section.rows.get(i);
        
      out.write("\n");
      out.write("        <tr class=\"");
      out.print( rowClasses[i % 2]);
      out.write("\">\n");
      out.write("            ");
  boolean boldface = false;
                for (String entry : row) {
                   if (entry.startsWith("\\")) { // Escaped start, just remove.
                       entry = entry.substring(1);
                   }
            
      out.write("\n");
      out.write("            <td class=\"tablecell\">");
      out.print( entry );
      out.write("</td>\n");
      out.write("            ");
 } 
      out.write("\n");
      out.write("        </tr>\n");
      out.write("        ");
 } 
      out.write("\n");
      out.write("    </table>\n");
      out.write("    ");
 } 
      out.write("\n");
      out.write("    <div class=\"prevnext\">\n");
      out.write("      <a href=\"#");
      out.print( id - 1 );
      out.write("\">Previous</a> | <a href=\"#");
      out.print( id + 1 );
      out.write("\">Next</a> |\n");
      out.write("      <a href=\"#top\">Top</a>\n");
      out.write("    </div>\n");
      out.write("    <p><br/></p>\n");
      out.write("    ");
 } 
      out.write("\n");
      out.write("\n");
      out.write("    <script id=\"source\" language=\"javascript\" type=\"text/javascript\">\n");
      out.write("$(function () {\n");
      out.write("    ");
 for (int id = 0; id < xan.sections.size(); id++) {
        View.Section section = xan.sections.get(id);
        int numCols = section.headers.size();
        if (!"line".equalsIgnoreCase(section.display))
            continue;
        // Get data for each series (column). Ignore x-axis, col 0
        for (int col=1; col < numCols; col++) {
    
      out.write("\n");
      out.write("            var data");
      out.print( id+1 );
      out.print( col );
      out.write(' ');
      out.write('=');
      out.write(' ');
      out.print( section.json.get(col-1) );
      out.write(";\n");
      out.write("        ");
 } 
      out.write("\n");
      out.write("        var xlabel");
      out.print( id );
      out.write(" = \"");
      out.print( section.headers.get(0) );
      out.write("\";\n");
      out.write("        var dataset = [");
      out.print( section.dataName );
      out.write("];\n");
      out.write("        var minx = ");
      out.print( section.min );
      out.write(";\n");
      out.write("        var maxx = ");
      out.print( section.max );
      out.write(";\n");
      out.write("        $.jqplot(\"graph");
      out.print( id );
      out.write("\", dataset,  {\n");
      out.write("            title: \"");
      out.print( section.name );
      out.write("\",\n");
      out.write("            axesDefaults: {\n");
      out.write("                    labelRenderer: $.jqplot.CanvasAxisLabelRenderer\n");
      out.write("            },\n");
      out.write("            seriesDefaults: {\n");
      out.write("                lineWidth: 1.75,\n");
      out.write("                location: 'e',\n");
      out.write("                placement: 'outside',\n");
      out.write("                rendererOptions: {\n");
      out.write("                    smooth: true\n");
      out.write("                }\n");
      out.write("            },\n");
      out.write("            series: [\n");
      out.write("            ");
 for (int j=1; j < numCols; j++) {
                if (j == 1) {
            
      out.write("\n");
      out.write("                    { label: \"");
      out.print( section.headers.get(j) );
      out.write("\", markerOptions:{show:false} }\n");
      out.write("                ");
 } else { 
      out.write("\n");
      out.write("                    , { label: \"");
      out.print( section.headers.get(j) );
      out.write("\", markerOptions:{show:false} }\n");
      out.write("                ");
 }
             }
      out.write("\n");
      out.write("\n");
      out.write("            ],\n");
      out.write("            axes: {\n");
      out.write("                xaxis: {\n");
      out.write("                label: xlabel");
      out.print( id );
      out.write(",\n");
      out.write("                ");
 if  (section.xIsTime == 1) {
                
      out.write("\n");
      out.write("                    renderer: $.jqplot.DateAxisRenderer,\n");
      out.write("                    tickOptions: {formatString:'%T'},\n");
      out.write("                    min: minx,\n");
      out.write("                    max: maxx,\n");
      out.write("                    pad: 1.3\n");
      out.write("                ");
 } 
      out.write("\n");
      out.write("                }\n");
      out.write("            },\n");
      out.write("            cursor: {\n");
      out.write("                show: true, showTooltip: true,\n");
      out.write("                followMouse: true,\n");
      out.write("                zoom: true\n");
      out.write("            },\n");
      out.write("            legend: {\n");
      out.write("                show: true\n");
      out.write("            }\n");
      out.write("        });\n");
      out.write("        //Hack to prevent jqplot from changing frame name in Chrome\n");
      out.write("        if(window.name=\"y9axis\"){\n");
      out.write("            window.name=\"display\";\n");
      out.write("        }\n");
      out.write("    ");
 } 
      out.write("\n");
      out.write("});\n");
      out.write("</script>\n");
      out.write("  </body>\n");
      out.write("</html>\n");
    } catch (Throwable t) {
      if (!(t instanceof SkipPageException)){
        out = _jspx_out;
        if (out != null && out.getBufferSize() != 0)
          out.clearBuffer();
        if (_jspx_page_context != null) _jspx_page_context.handlePageException(t);
      }
    } finally {
      if (_jspxFactory != null) _jspxFactory.releasePageContext(_jspx_page_context);
    }
  }
}
