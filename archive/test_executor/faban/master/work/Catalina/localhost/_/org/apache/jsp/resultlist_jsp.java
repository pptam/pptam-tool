package org.apache.jsp;

import javax.servlet.*;
import javax.servlet.http.*;
import javax.servlet.jsp.*;
import com.sun.faban.harness.webclient.RunResult;
import com.sun.faban.common.SortableTableModel;
import com.sun.faban.common.SortDirection;
import com.sun.faban.harness.webclient.TagEngine;
import java.util.StringTokenizer;
import java.io.File;
import java.io.*;
import java.util.Set;
import java.util.*;
import java.net.URLEncoder;
import com.sun.faban.harness.common.Config;

public final class resultlist_jsp extends org.apache.jasper.runtime.HttpJspBase
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
      out.write(" * $Id$\n");
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
    SortableTableModel resultTable = (SortableTableModel)request.getAttribute("table.model");
    String feedURL = (String)request.getAttribute("feedURL");
    String tagInSearch = (String)request.getAttribute("tagInSearch");
    String sortDirection = "DESCENDING";
    //String sort = "<img src=/img/sort_desc.gif></img>";
    int rows;
    if (resultTable != null && (rows = resultTable.rows()) > 0) {
    
      out.write("\n");
      out.write("<html>\n");
      out.write("    <head>\n");
      out.write("        <meta http-equiv=\"Content-Type\" content=\"text/html; charset=iso-8859-1\"/>\n");
      out.write("        <meta name=\"Author\" content=\"Ramesh Ramachandran\"/>\n");
      out.write("        <meta name=\"Description\" content=\"Reults JSP\"/>\n");
      out.write("        <title>Benchmark Results [");
      out.print( Config.FABAN_HOST );
      out.write("]</title>\n");
      out.write("        <link rel=\"icon\" type=\"image/gif\" href=\"/img/faban.gif\"/>\n");
      out.write("        <link rel=\"alternate\" type=\"application/atom+xml\" title=\"Atom Feed\" href=\"");
      out.print( feedURL );
      out.write("\"/>\n");
      out.write("        <link rel=\"stylesheet\" type=\"text/css\" href=\"/css/style.css\" />\n");
      out.write("        <link rel=\"stylesheet\" type=\"text/css\" href=\"/css/balloontip2.css\" />\n");
      out.write("        <script type=\"text/javascript\" src=\"/scripts/balloontip2.js\"></script>\n");
      out.write("    </head>\n");
      out.write("    <body>\n");
      out.write("        <div style=\"text-align: right;\"><a\n");
      out.write("             href=\"");
      out.print( feedURL );
      out.write("\"><img\n");
      out.write("             style=\"border: 0px solid ; width: 16px; height: 16px;\"\n");
      out.write("             alt=\"Feed\" src=\"/img/feed.gif\"></a></div>\n");
      out.write("\n");
      out.write("            <form name=\"processrun\" method=\"post\" action=\"/controller/result_action/take_action\">\n");
      out.write("              <center>\n");
      out.write("                <input type=\"submit\" name=\"process\" value=\"Delete\">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;\n");
      out.write("                <input type=\"submit\" name=\"process\" value=\"Compare\">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;\n");
      out.write("                <!-- Commented out until FenXi supports averaging again.\n");
      out.write("                <input type=\"submit\" name=\"process\" value=\"Average\">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;\n");
      out.write("                -->\n");
      out.write("    ");

            boolean allowArchive = false;
            if (Config.repositoryURLs != null &&
                Config.repositoryURLs.length > 0)
                allowArchive = true;

            if (allowArchive) {
    
      out.write("\n");
      out.write("                <input type=\"submit\" name=\"process\" value=\"Archive\">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;\n");
      out.write("    ");

            }
    
      out.write("\n");
      out.write("                <input type=\"reset\">\n");
      out.write("              </center>\n");
      out.write("              <br>\n");
      out.write("              <table id=\"ResultTable\" BORDER=0 CELLPADDING=4 CELLSPACING=3 width=\"90%\" align=\"center\" style=\"padding:2px; border: 2px solid #cccccc;\">\n");
      out.write("              <tbody>\n");
      out.write("              <tr>\n");
      out.write("                  <th class=\"header\">&nbsp;</th>\n");
      out.write("    ");
      // Last column (column 8) contaiuns the URL to the results.
            for (int i = 0; i < resultTable.columns() - 1; i++) {
                  if(resultTable.getSortDirection() == SortDirection.DESCENDING){
                      sortDirection = "ASCENDING";
                  }else if(resultTable.getSortDirection() == SortDirection.ASCENDING){
                      sortDirection = "DESCENDING";
                  }
                  String sortLink = "/controller/results/list?sortColumn=" + i + "&sortDirection=" + sortDirection.trim();
                  if(tagInSearch != null && tagInSearch.length() > 0)
                      sortLink = "/controller/results/list?inputtag="+ tagInSearch.trim() +"&sortColumn=" + i + "&sortDirection=" + sortDirection.trim();
    
      out.write("\n");
      out.write("                  <th class=\"header\"><a href=\"");
      out.print( sortLink );
      out.write("\" target=\"main\">");
      out.print( resultTable.getHeader(i));
      out.write("</a></th>\n");
      out.write("    ");
      } 
      out.write("\n");
      out.write("              </tr>\n");
      out.write("    ");

            final String[] rowClasses = { "even", "odd" };
            for(int i = 0; i < rows; i++) {
                Comparable[] row = resultTable.getRow(i);
                String rowClass = rowClasses[i % 2];
    
      out.write("\n");
      out.write("            <tr class=\"");
      out.print( rowClass );
      out.write("\" onmouseover=\"this.className='highlight'\"\n");
      out.write("                 onmouseout=\"this.className='");
      out.print( rowClass );
      out.write("'\">\n");
      out.write("                <td class=\"tablecell\" ><input type=\"checkbox\" name=\"select\" value=\"");
      out.print( row[0] );
      out.write("\"></input></td>\n");
      out.write("    ");
          String linkURL = row[8].toString();
                String onclick = "";
                if (linkURL != null && linkURL.length() > 0)
                    onclick = "onclick=\"location.href='" + linkURL + "'\"";
                for (int j = 0; j < row.length - 1; j++) { // Again, last is URL
                    String mouseover = " ";                    
                    if(row[j] == null)
                       row[j] = " ";
                    String val = row[j].toString();
                    if(j==0 || j==1 || "&nbsp;".equals(row[j].toString()) || "&nbsp".equals(row[j].toString())){
      out.write("\n");
      out.write("                       <td class=\"tablecell\" ");
      out.print( onclick );
      out.write('>');
      out.print(val);
      out.write("</td>\n");
      out.write("                    ");
} else if (j == 2) { 
      out.write("                             \n");
      out.write("                             <td class=\"tablecell\" ");
      out.print( onclick );
      out.write(' ');
      out.print( mouseover);
      out.write('>');
      out.print(val);
      out.write("</td>\n");
      out.write("                    ");
}else{                      
                         if(row[j] != null) {
                             StringBuilder formattedStr = new StringBuilder();
                             StringTokenizer t = new StringTokenizer(row[j].toString());
                             val = t.nextToken().trim();
                             while (t.hasMoreTokens()) {
                                formattedStr.append(t.nextToken().trim() + " ");
                             }
                             mouseover = "onmouseover=\"showtip('" + val + " " + formattedStr.toString()+ "')\" onmouseout=\"hideddrivetip()\"";
                             
      out.write("\n");
      out.write("                             ");
if (j == (row.length - 2)) { // The tag column 
      out.write("\n");
      out.write("                                 ");
 if (row[j].toString().length() > val.length()){ 
      out.write("\n");
      out.write("                                    <td class=\"tablecell\" ");
      out.print( onclick );
      out.write(' ');
      out.print( mouseover);
      out.write('>');
      out.print(val);
      out.write(".....</td>\n");
      out.write("                                 ");
 }else {
      out.write("\n");
      out.write("                                    <td class=\"tablecell\" ");
      out.print( onclick );
      out.write('>');
      out.print(val);
      out.write("</td>\n");
      out.write("                             ");
  }
                             } else {
      out.write("\n");
      out.write("                                <td class=\"tablecell\" ");
      out.print( onclick );
      out.write(' ');
      out.print( mouseover);
      out.write('>');
      out.print(val);
      out.write("</td>\n");
      out.write("                             ");
 }
                         }
      out.write("\n");
      out.write("   ");
                }
                } 
      out.write("\n");
      out.write("            </tr>\n");
      out.write("    ");
      } 
      out.write("\n");
      out.write("     </tbody>\n");
      out.write("     </table>\n");
      out.write("     <br/>\n");
      out.write("     <br/>\n");
      out.write("     <center>\n");
      out.write("     <input type=\"submit\" name=\"process\" value=\"Delete\">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;\n");
      out.write("     <input type=\"submit\" name=\"process\" value=\"Compare\">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;\n");
      out.write("     <!-- Commented out until FenXi supports averaging again.\n");
      out.write("     <input type=\"submit\" name=\"action\" value=\"edit_average>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;\n");
      out.write("     -->\n");
      out.write("    ");

            if (allowArchive) {
    
      out.write("\n");
      out.write("                <input type=\"submit\" name=\"process\" value=\"Archive\">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;\n");
      out.write("    ");

            }
    
      out.write("\n");
      out.write("     <input type=\"reset\">\n");
      out.write("     </center>\n");
      out.write("    </form>\n");
      out.write("    ");

    } else {
    
      out.write("\n");
      out.write("            <br/>\n");
      out.write("            <center><b>There are no results</b></center>\n");
      out.write("            <br/>\n");
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
