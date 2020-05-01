package org.apache.jsp;

import javax.servlet.*;
import javax.servlet.http.*;
import javax.servlet.jsp.*;
import com.sun.faban.harness.webclient.RunResult;
import com.sun.faban.common.SortableTableModel;
import java.io.File;
import java.io.*;
import java.util.Set;
import java.util.*;
import java.net.URLEncoder;
import com.sun.faban.harness.common.Config;

public final class runinfo_jsp extends org.apache.jasper.runtime.HttpJspBase
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
      out.write("<!--\n");
      out.write("/* The contents of this file are subject to the terms\n");
      out.write(" * of the Common Development and Distribution License\n");
      out.write(" * (the License). You may not use this file except in\n");
      out.write(" * compliance with the License.\n");
      out.write(" *\n");
      out.write(" * You can obtain a copy of the License at\n");
      out.write(" * http://www.sun.com/cddl/cddl.html or\n");
      out.write(" * install_dir/legal/LICENSE\n");
      out.write(" * See the License for the specific language governing\n");
      out.write(" * permission and limitations under the License.\n");
      out.write(" *\n");
      out.write(" * When distributing Covered Code, include this CDDL\n");
      out.write(" * Header Notice in each file and include the License file\n");
      out.write(" * at install_dir/legal/LICENSE.\n");
      out.write(" * If applicable, add the following below the CDDL Header,\n");
      out.write(" * with the fields enclosed by brackets [] replaced by\n");
      out.write(" * your own identifying information:\n");
      out.write(" * \"Portions Copyrighted [year] [name of copyright owner]\"\n");
      out.write(" *\n");
      out.write(" * Copyright 2005-2009 Sun Microsystems Inc. All Rights Reserved\n");
      out.write(" */\n");
      out.write("-->\n");
      out.write("    \n");
      out.write("    ");
      com.sun.faban.harness.webclient.UserEnv usrEnv = null;
      synchronized (session) {
        usrEnv = (com.sun.faban.harness.webclient.UserEnv) _jspx_page_context.getAttribute("usrEnv", PageContext.SESSION_SCOPE);
        if (usrEnv == null){
          usrEnv = new com.sun.faban.harness.webclient.UserEnv();
          _jspx_page_context.setAttribute("usrEnv", usrEnv, PageContext.SESSION_SCOPE);
        }
      }
      out.write("\n");
      out.write("    ");

    response.setHeader("Cache-Control", "no-cache");
    String[] header = (String[])request.getAttribute("header");
    String[] row = (String[])request.getAttribute("runinfo");
    if (row != null) {
    
      out.write("\n");
      out.write("\n");
      out.write("\n");
      out.write("<html>\n");
      out.write("    <head>\n");
      out.write("        <meta http-equiv=\"Content-Type\" content=\"text/html; charset=iso-8859-1\"/>\n");
      out.write("        <meta name=\"Author\" content=\"Sheetal Patil\"/>\n");
      out.write("        <title>Run Info [");
      out.print( Config.FABAN_HOST );
      out.write("]</title>\n");
      out.write("        <link rel=\"icon\" type=\"image/gif\" href=\"/img/faban.gif\"/>\n");
      out.write("        <link rel=\"stylesheet\" type=\"text/css\" href=\"/css/style.css\" />\n");
      out.write("        <script type=\"text/javascript\">\n");
      out.write("            var editing = false;\n");
      out.write("            function editText(td_id) {\n");
      out.write("                editing = true;\n");
      out.write("                var td = document.getElementById(td_id);\n");
      out.write("                var tddiv = document.getElementById(td_id+\"div\");\n");
      out.write("                var content = tddiv.innerHTML;\n");
      out.write("                td.innerHTML = '<textarea id=\"txtarea\" class=\"editing\" >'+ content +'</textarea><br><input type=\"button\" id=\"save\" onclick=\"saveEdit(\\'' + td_id + '\\', \\'txtarea\\')\" value=\"Save\"></input> <input type=\"button\" id=\"cancel\" onclick=\"cancelEdit(\\'' + td_id + '\\', \\'' + content + '\\')\" value=\"Cancel\"></input>';\n");
      out.write("            }\n");
      out.write("\n");
      out.write("            function checkIfEditing() {\n");
      out.write("                return editing;\n");
      out.write("            }\n");
      out.write("\n");
      out.write("            function saveEdit(td_id, textarea) {\n");
      out.write("                var td = document.getElementById(td_id);\n");
      out.write("                var content = document.getElementById(textarea).value;\n");
      out.write("                td.innerHTML = '<div id=\"' + td_id + 'div\" onclick=\"if (checkIfEditing() == false) editText(\\'' + td_id + '\\');\">' + content + '</div>';\n");
      out.write("                if(td_id == \"Tags\"){\n");
      out.write("                    updateTags(content);\n");
      out.write("                }\n");
      out.write("                if(td_id == \"Description\"){\n");
      out.write("                    updateDescription(content);\n");
      out.write("                }\n");
      out.write("                editing = false;\n");
      out.write("\n");
      out.write("            }\n");
      out.write("\n");
      out.write("            function cancelEdit(td_id, content) {\n");
      out.write("                var td = document.getElementById(td_id);\n");
      out.write("                td.innerHTML = '<div id=\"' + td_id + 'div\" onclick=\"if (checkIfEditing() == false) editText(\\'' + td_id + '\\');\">' + content + '</div>'  ;\n");
      out.write("                editing = false;\n");
      out.write("            }\n");
      out.write("\n");
      out.write("            var updateTagsURL = \"/controller/uploader/update_tags_file?tags=\";\n");
      out.write("            function updateTags(content) {\n");
      out.write("                http.open(\"GET\", updateTagsURL + escape(content) + \"&runId=\" + escape('");
      out.print(row[0]);
      out.write("'), true);\n");
      out.write("                http.send(null);\n");
      out.write("            }\n");
      out.write("\n");
      out.write("            var updateDescURL = \"/controller/uploader/update_run_desc?desc=\";\n");
      out.write("            function updateDescription(content) {\n");
      out.write("                http.open(\"GET\", updateDescURL + escape(content) + \"&runId=\" + escape('");
      out.print(row[0]);
      out.write("'), true);\n");
      out.write("                http.send(null);\n");
      out.write("            }\n");
      out.write("\n");
      out.write("            function getHTTPObject() {\n");
      out.write("                var xmlhttp;\n");
      out.write("                if (!xmlhttp && typeof XMLHttpRequest != 'undefined') {\n");
      out.write("                    try {\n");
      out.write("                        xmlhttp = new XMLHttpRequest();\n");
      out.write("                    } catch (e) {\n");
      out.write("                        xmlhttp = false;\n");
      out.write("                    }\n");
      out.write("                }\n");
      out.write("                return xmlhttp;\n");
      out.write("            }\n");
      out.write("            var http = getHTTPObject();\n");
      out.write("        </script>\n");
      out.write("    </head>\n");
      out.write("    <body>\n");
      out.write("        <div id=\"edit\"></div>\n");
      out.write("        <table BORDER=0 CELLPADDING=4 CELLSPACING=3 style=\"padding:2px; border: 2px solid #cccccc; width:250px; height:100px;\">\n");
      out.write("            <tbody>\n");
      out.write("                ");
 for (int j = 0; j < row.length; j++) {
      out.write("\n");
      out.write("                <tr ");
if (j % 2 == 0) {
      out.write("class=\"even\"");
} else {
      out.write("class=\"odd\"");
 }
      out.write(">\n");
      out.write("                    <td class=\"tablecell\">");
      out.print( header[j]);
      out.write("</td>\n");
      out.write("                    ");
if(header[j].equals("Description") || header[j].equals("Tags")){
      out.write("\n");
      out.write("                        <td id=\"");
      out.print( header[j] );
      out.write("\" class=\"tablecell\"><div id=\"");
      out.print( header[j] );
      out.write("div\" onclick=\"if (checkIfEditing() == false) editText('");
      out.print( header[j] );
      out.write("');\">");
      out.print(row[j]);
      out.write("</div></td>\n");
      out.write("                    ");
}else{
      out.write("\n");
      out.write("                        <td id=\"");
      out.print( header[j] );
      out.write("\" class=\"tablecell\" >");
      out.print(row[j]);
      out.write("</td>\n");
      out.write("                    ");
}
      out.write("\n");
      out.write("                </tr>\n");
      out.write("                ");
      }
      out.write("\n");
      out.write("            </tbody>\n");
      out.write("        </table>\n");
      out.write("    ");
} 
      out.write("\n");
      out.write("    </body>\n");
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
