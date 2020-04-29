package org.apache.jsp;

import javax.servlet.*;
import javax.servlet.http.*;
import javax.servlet.jsp.*;
import java.io.FileReader;
import com.sun.faban.harness.common.Config;
import com.sun.faban.harness.ParamRepository;
import java.io.File;
import com.sun.faban.harness.common.BenchmarkDescription;
import java.util.*;
import com.sun.faban.harness.webclient.RunResult;
import com.sun.faban.harness.common.HostRoles;

public final class statsnavigator_jsp extends org.apache.jasper.runtime.HttpJspBase
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
      out.write(" /**\n");
      out.write("  * Modified by Shanti Subramanyam to support graphing through xan_view\n");
      out.write("  */\n");
      out.write("-->\n");
      out.write("\n");

    String runId = request.getParameter("runId");
    String[] statusFileContent = RunResult.readStatus(runId);
    boolean finished = true;
    if ("STARTED".equals(statusFileContent[0]))
        finished = false;

    // Now check the output files...
    File outDir = new File(Config.OUT_DIR + runId);
    // Tool output file pattern is <tool>.log.<host>[suffix]
    String[] suffixes = { ".html", ".htm", "" }; // The empty string always last
    String[] htmlSuffixes = { ".html", ".htm" };
    TreeSet<String> allHosts = new TreeSet<String>();
    TreeSet<String> allTools = new TreeSet<String>();
    
    // This map maps the short host name to the one used in the file name.
    HashMap<String, String> infoHostMap = new HashMap<String, String>();

    // The toolHostMap maps host:tool to the actual stats file name.
    HashMap<String, ArrayList<String>> toolHostMap =
            new HashMap<String, ArrayList<String>>();

    File hosttypes = new File(outDir, "META-INF");
    hosttypes = new File(hosttypes, "hosttypes");
    HostRoles hostRoles = null;
    if (hosttypes.isFile()) {
        hostRoles = new HostRoles(hosttypes.getAbsolutePath());
    }

    // These are known files that have file names looking like tool output.
    // They should be ignored.
    HashSet<String> ignoreFiles = new HashSet<String>();
    ignoreFiles.add("driver.log.lck");
    ignoreFiles.add("log.xml.lck");

    fileSearchLoop:
    for (String fileName : outDir.list()) {
        // Screen out all image files, hidden files, and files to be ignored...
        if (fileName.endsWith(".png") || fileName.endsWith(".jpg") ||
            fileName.endsWith(".jpeg") || fileName.endsWith(".gif") ||
            fileName.startsWith(".") || ignoreFiles.contains(fileName))
            continue;

        // Then proces the sysinfo files...
        if (fileName.startsWith("sysinfo.")) {
            String hostName = fileName.substring(8, fileName.length() - 5);
            infoHostMap.put(hostName, hostName); // Points to it's own name
            allHosts.add(hostName);

        // Process the real stats files.
        } else {
            int logIdx = fileName.indexOf(".log.");
            if (logIdx == -1) // New FenXi files need to be .xan.
                logIdx = fileName.indexOf(".xan.");
            if (logIdx == -1) // summary.xml.hostname case
                logIdx = fileName.indexOf(".xml.");
            if (logIdx == -1)
                continue;
            String toolName = fileName.substring(0, logIdx);
            String hostName = null;

            // Grab the host name from file name, based on suffix
            for (String suffix : suffixes) {
                int suffixSize = suffix.length();
                if (suffixSize == 0 || fileName.endsWith(suffix)) {
                    int hostBegin = logIdx + 5;
                    int hostEnd = fileName.length() - suffixSize;
                    // if the host name part is missing, it is not a stat file.
                    if (hostBegin >= hostEnd)
                        continue fileSearchLoop;
                    hostName = fileName.substring(hostBegin, hostEnd);
                    int idx = hostName.indexOf('.');
                    if (idx > 0)
                        hostName = hostName.substring(0, idx);

                    break;
                }
            }

            if (hostRoles != null) { // Map the alias to the actual host name
                hostName = hostRoles.getHostByAlias(hostName);
            } else { // No roles? Drop the domain part of the host.
                int domainIdx = hostName.indexOf('.');
                if (domainIdx != -1) {
                    String fullName = hostName;
                    hostName = fullName.substring(0, domainIdx);
                }
            }
            if (hostName == null) {
                response.sendError(500, "Error mapping stats. Offending file: "
                                        + fileName);
                return;
            }

            String toolHostKey = hostName + ':' + toolName;
            ArrayList<String> toolHostFiles = toolHostMap.get(toolHostKey);
            if (toolHostFiles == null) {
                toolHostFiles = new ArrayList<String>(2);
                toolHostMap.put(toolHostKey, toolHostFiles);
            }
            toolHostFiles.add(fileName);
            allHosts.add(hostName);
            allTools.add(toolName);
        }
    }

      out.write("\n");
      out.write("<html>\n");
      out.write("    <head>\n");
      out.write("        <title>Statistics for Run ");
      out.print(runId);
      out.write(' ');
      out.write('[');
      out.print( Config.FABAN_HOST );
      out.write("]</title>\n");
      out.write("        <link rel=\"icon\" type=\"image/gif\" href=\"img/faban.gif\">\n");
      out.write("        ");
 if (!finished) { 
      out.write("\n");
      out.write("            <meta http-equiv=\"refresh\" content=\"10\">\n");
      out.write("        ");
 } 
      out.write("\n");
      out.write("        ");

            String[] hosts;
            if (hostRoles != null) { // If we know the roles, order by relevance in that role.
                hosts = hostRoles.getHostsInOrder();
        
      out.write("\n");
      out.write("        <link rel=\"stylesheet\" type=\"text/css\" href=\"/css/style.css\" />        \n");
      out.write("        <link rel=\"stylesheet\" type=\"text/css\" href=\"css/balloontip2.css\" />\n");
      out.write("        <script type=\"text/javascript\" src=\"scripts/balloontip2.js\"></script>\n");
      out.write("         ");

            } else { // If we don't know the roles, order by name
                hosts = new String[allHosts.size()];
                hosts = allHosts.toArray(hosts);
            }
         
      out.write("\n");
      out.write("    </head>\n");
      out.write("    <body>\n");
      out.write("        ");

            if (hostRoles != null)
                for (String hostName : hosts) {
                    String[] roles = hostRoles.getRolesByHost(hostName);
        
      out.write("\n");
      out.write("        <div id=\"");
      out.print( hostName );
      out.write("_balloon\" class=\"ballooncontent\">\n");
      out.write("        ");

                    StringBuilder b = new StringBuilder();
                    for (String role : roles) {
                        String[] aliases = hostRoles.getAliasesByHostAndRole(hostName, role);
                        if (aliases.length == 0)
                            aliases = null;
                        if (aliases.length == 1 && hostName.equals(aliases[0]))
                            aliases = null;
                        b.append("<b>").append(role).append("</b>");
                        if (aliases != null) {
                            b.append(": ").append(aliases[0]);
                            for (int i = 1; i < aliases.length; i++)
                                b.append(", ").append(aliases[i]);
                        }
                        b.append("<br/>");
                    }
                    out.print(b.toString());
        
      out.write("\n");
      out.write("        </div>\n");
      out.write("        ");
      } 
      out.write("\n");
      out.write("        <table border=\"0\" cellpadding=\"4\" cellspacing=\"3\"\n");
      out.write("            style=\"padding: 2px; border: 2px solid #cccccc; text-align: center; width: 80%;\">\n");
      out.write("\n");
      out.write("            ");
 if (allHosts.size() == 0) {
                    if (!finished) {
            
      out.write("\n");
      out.write("                <h2><center>Statistics not yet available.</center></h2>\n");
      out.write("            ");
      } else { 
      out.write("\n");
      out.write("                <h2><center>Statistics not available for this run.</center></h2>\n");
      out.write("            ");
      }
               } else { 
      out.write("\n");
      out.write("                 <tbody>\n");
      out.write("                 <tr>\n");
      out.write("                     <th class=\"header\">System</th>\n");
      out.write("                     ");
 for (String tool : allTools) { 
      out.write("\n");
      out.write("                        <th class=\"header\">");
      out.print( tool );
      out.write("</th>\n");
      out.write("                     ");
 } 
      out.write("\n");
      out.write("                 </tr>\n");
      out.write("                 ");
 String[] rowclass = { "even", "odd" };
                    String path = "/output/" + runId + '/';
                    String xanPath = "/controller/view/xan_view/" + runId + '/';
                    ArrayList<String> htmlFiles = new ArrayList<String>(1);
                    ArrayList<String> graphLinks = new ArrayList<String>(1);

                    for (int i = 0; i < hosts.length; i++) {
                        String mouseover = "";
                        if (hostRoles != null) {
                            mouseover = "onmouseover=\"ddrivetip('" + hosts[i] +
                                    "_balloon')\" onmouseout=\"hideddrivetip()\"";
                        }
                 
      out.write("\n");
      out.write("                 <tr class=\"");
      out.print( rowclass[i % 2] );
      out.write('"');
      out.write(' ');
      out.print( mouseover);
      out.write(">\n");
      out.write("                     ");
 String fullName = infoHostMap.get(hosts[i]);
                        if (fullName != null) {
                     
      out.write("\n");
      out.write("                        <td class=\"tablecell\" style=\"text-align: left;\"><a href=\"");
      out.print( path );
      out.write("sysinfo.");
      out.print( fullName );
      out.write(".html\">");
      out.print( hosts[i] );
      out.write("</a></td>\n");
      out.write("                     ");
 } else { 
      out.write("\n");
      out.write("                        <td class=\"tablecell\" style=\"text-align: left;\">");
      out.print( hosts[i] );
      out.write("</td>\n");
      out.write("                     ");
 }
                        for (String tool : allTools) {
                            ArrayList<String> toolHostFiles = toolHostMap.get(
                                                    hosts[i] + ':' + tool);
                            if (toolHostFiles != null && toolHostFiles.size() > 0) {
                     
      out.write("\n");
      out.write("                                <td class=\"tablecell\" style=\"text-align: center;\">\n");
      out.write("                                ");

                                // Separate html files out from the raw files in toolHostFiles.
                                toolFileLoop:
                                for (Iterator<String> iter = toolHostFiles.iterator(); iter.hasNext();) {
                                    String fileName = iter.next();
                                    if (fileName.indexOf(".xan.") > 0 || fileName.endsWith(".xan")) {
                                        iter.remove();
                                        graphLinks.add(fileName);
                                    }
                                    else if (fileName.endsWith(".html") || fileName.endsWith(".htm")) {
                                        iter.remove();
                                        htmlFiles.add(fileName);
                                    } else {
                                        // For each of the raw files, there might be an
                                        // html file in the post directory. Check that.
                                        String htmlFileName = Config.POST_DIR + fileName;
                                        for (String suffix : htmlSuffixes) {
                                            String tryFileName = htmlFileName + suffix;
                                            File htmlFile = new File(outDir, tryFileName);
                                            if (htmlFile.exists()) {
                                                htmlFiles.add(tryFileName);
                                                continue toolFileLoop;
                                            }
                                        }
                                    }
                                }
                                // Do the graph link
                                for (String fileName : graphLinks) {
                                
      out.write("\n");
      out.write("                                    <small><i><a href=\"");
      out.print( xanPath + fileName );
      out.write("\">graphs</a></i></small>\n");
      out.write("                                ");
 }
                                graphLinks.clear();

                                // Do the html link
                                for (String fileName : htmlFiles) { 
      out.write("\n");
      out.write("                                    <small><i><a href=\"");
      out.print( path + fileName );
      out.write("\">html</a></i></small>\n");
      out.write("                             ");
 }
                                htmlFiles.clear();

                                // Do the raw link
                                for (String fileName : toolHostFiles) { 
      out.write("\n");
      out.write("                                    <small><i><a href=\"");
      out.print( path + fileName );
      out.write("\">raw</a></i></small>\n");
      out.write("                             ");
 }
                     
      out.write("\n");
      out.write("                                </td>\n");
      out.write("                     ");
     } else {    
      out.write("\n");
      out.write("                                <td class=\"tablecell\">&nbsp;</td>\n");
      out.write("                     ");

                            }
                        }
                     }
                     
      out.write("\n");
      out.write("                 </tr>\n");
      out.write("                 </tbody>\n");
      out.write("             ");
 } 
      out.write("\n");
      out.write("         </table>\n");
      out.write("    </body>\n");
      out.write("</html>\n");
      out.write("\n");
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
