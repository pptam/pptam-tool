package org.apache.jsp;

import javax.servlet.*;
import javax.servlet.http.*;
import javax.servlet.jsp.*;
import java.util.Map;
import java.util.HashMap;
import java.io.File;
import javax.security.auth.Subject;
import com.sun.faban.harness.util.FileHelper;
import com.sun.faban.harness.common.Config;
import com.sun.faban.harness.common.BenchmarkDescription;
import com.sun.faban.harness.security.AccessController;
import com.sun.faban.harness.webclient.UserEnv;

public final class selectprofile_jsp extends org.apache.jasper.runtime.HttpJspBase
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
      out.write("\n");
      out.write("\n");
      com.sun.faban.harness.webclient.UserEnv usrEnv = null;
      synchronized (session) {
        usrEnv = (com.sun.faban.harness.webclient.UserEnv) _jspx_page_context.getAttribute("usrEnv", PageContext.SESSION_SCOPE);
        if (usrEnv == null){
          usrEnv = new com.sun.faban.harness.webclient.UserEnv();
          _jspx_page_context.setAttribute("usrEnv", usrEnv, PageContext.SESSION_SCOPE);
        }
      }
      out.write("\n");
      out.write("<html>\n");
      out.write("     <head>\n");
      out.write("         <link rel=\"icon\" type=\"image/gif\" href=\"img/faban.gif\">\n");
      out.write("         <link rel=\"stylesheet\" type=\"text/css\" href=\"/css/style.css\" />\n");
      out.write("         <meta http-equiv=\"Content-Type\" content=\"text/html; charset=iso-8859-1\"/>\n");
      out.write("         <meta name=\"Author\" content=\"Ramesh Ramachandran\"/>\n");
      out.write("         <meta name=\"Description\" content=\"Form to display profile selection\"/>\n");
      out.write("         <title>Select Profile [");
      out.print( Config.FABAN_HOST );
      out.write("]</title>\n");
  String tagsForProfile = "";
    File tagsFile = null;
    String profile = (String)session.getAttribute("faban.profile");
    
    
    BenchmarkDescription desc =  (BenchmarkDescription) session.getAttribute(
            "faban.benchmark");
    String benchmark = desc == null ? null : desc.name;
    Subject user = usrEnv.getSubject();

    if(profile != null && benchmark != null && 
       AccessController.isSubmitAllowed(user, desc.shortName)) {

      out.write("\n");
      out.write("         <meta HTTP-EQUIV=REFRESH CONTENT=\"0;URL=new-run.jsp\">\n");

    }
    else {
        String[] profiles = usrEnv.getProfiles();
        if(profile == null){
            if((profiles != null) && (profiles.length > 0)) {
                profile = profiles[0];
                tagsFile = new File(Config.PROFILES_DIR + profile + "/tags");
                if(tagsFile.exists() && tagsFile.length()>0){
                    tagsForProfile = FileHelper.readContentFromFile(tagsFile).trim();
                }
            }
        }
        
        Map<String, BenchmarkDescription> benchNameMap =
                BenchmarkDescription.getBenchNameMap();
        // We need to ensure only benchmarks the user is allowed to submit are shown.
        // The benchNameMap is a reference to the cached version. Don't change it.
        // Make copies instead.
        HashMap<String, BenchmarkDescription> allowedBench = 
                new HashMap<String, BenchmarkDescription>(benchNameMap.size());
        for (Map.Entry<String, BenchmarkDescription> entry : benchNameMap.entrySet()) {
            BenchmarkDescription d = entry.getValue();
            if (AccessController.isSubmitAllowed(user, d.shortName))
                allowedBench.put(entry.getKey(), d);
        }
        int benchCount = allowedBench.size();
        if (benchNameMap.size() < 1) {

      out.write("\n");
      out.write("    </head>\n");
      out.write("    <body>\n");
      out.write("<h3><center>Sorry, Faban could not find or successfully deploy any benchmarks.</center></h3>\n");

        } else if (benchCount < 1) {

      out.write("\n");
      out.write("</head>\n");
      out.write("<body>\n");
      out.write("<h3><center>Sorry, you're not allowed to submit any benchmark.</center></h3>\n");

        } else {
            String[] benchmarks = new String[benchCount];
            benchmarks = allowedBench.keySet().toArray(benchmarks);

      out.write("\n");
      out.write("\n");
      out.write("\n");
      out.write("<script>\n");
      out.write("var req;\n");
      out.write("function updateProfile() {\n");
      out.write("    document.bench.profile.value=document.bench.profilelist.value;\n");
      out.write("    var url = \"/controller/result_action/profile_tag_list?profileselected=\"+escape(document.bench.profile.value);\n");
      out.write("    if (typeof XMLHttpRequest != \"undefined\") {\n");
      out.write("       req = new XMLHttpRequest();\n");
      out.write("   } else if (window.ActiveXObject) {\n");
      out.write("       req = new ActiveXObject(\"Microsoft.XMLHTTP\");\n");
      out.write("   }\n");
      out.write("   req.open(\"GET\", url, true);\n");
      out.write("   req.onreadystatechange = callback;\n");
      out.write("   req.send(null);\n");
      out.write("}\n");
      out.write("\n");
      out.write("function callback() {\n");
      out.write("    if (req.readyState == 4) {\n");
      out.write("        if (req.status == 200) {\n");
      out.write("            //update tags field\n");
      out.write("            var result = req.responseText;\n");
      out.write("            document.getElementById(\"tags\").innerHTML=result;\n");
      out.write("        }\n");
      out.write("    }\n");
      out.write("}\n");
      out.write("\n");
      out.write("</script>\n");
      out.write("\n");
      out.write("</head>\n");
      out.write("<body>\n");
      out.write("<br/>\n");
      out.write("<br/>\n");
      out.write("<br/>\n");
      out.write("\n");
      out.write("<form name=\"bench\" method=\"post\" action=\"new-run.jsp\">\n");
      out.write("  <table cellpadding=\"0\" cellspacing=\"2\" border=\"0\" align=\"center\">\n");
      out.write("    <tbody>\n");
      out.write("      <tr>\n");
      out.write("        <td>Profile</td>\n");
      out.write("        <td>\n");
      out.write("          ");
 if(profile != null) { 
      out.write("\n");
      out.write("            <input type=\"text\" title=\"Please select profile or enter new profile name\"\n");
      out.write("                name=\"profile\" size=\"10\" value=");
      out.print(profile );
      out.write(" >\n");
      out.write("            <select name=\"profilelist\" title=\"Please select profile or enter new profile name\"\n");
      out.write("                ONCHANGE=\"updateProfile()\">\n");
      out.write("              ");
 for(int i = 0; i < profiles.length; i++) { 
      out.write("\n");
      out.write("                <option\n");
      out.write("                  ");
 if(((profile != null) && profiles[i].equals(profile)) ||
                        ((profile == null) && (i == 0))){ 
      out.write("\n");
      out.write("                    SELECTED\n");
      out.write("                  ");
 } 
      out.write("\n");
      out.write("                  >");
      out.print( profiles[i]);
      out.write("\n");
      out.write("                </option>\n");
      out.write("              ");
 } 
      out.write("\n");
      out.write("            </select>\n");
      out.write("          ");
 } else { 
      out.write("\n");
      out.write("            <input type=\"text\" title=\"Please enter new profile name for your runs\"\n");
      out.write("                name=\"profile\" size=\"10\">\n");
      out.write("          ");
 } 
      out.write("\n");
      out.write("        </td>\n");
      out.write("      </tr>\n");
      out.write("      ");
 if (benchmark == null)
             benchmark = benchmarks[0];
         if (benchmarks.length > 1) { 
      out.write("\n");
      out.write("        <tr>\n");
      out.write("          <td>Benchmark</td>\n");
      out.write("          <td>\n");
      out.write("            <select name=\"benchmark\" title=\"Please select benchmark to run\">\n");
      out.write("              ");
 for (int i = 0; i < benchmarks.length; i++) { 
      out.write("\n");
      out.write("              <option\n");
      out.write("                  ");
 if(benchmarks[i].equals(benchmark)) { 
      out.write("\n");
      out.write("                    SELECTED\n");
      out.write("                  ");
 } 
      out.write("\n");
      out.write("                  >");
      out.print( benchmarks[i]);
      out.write("\n");
      out.write("              ");
 } 
      out.write("\n");
      out.write("            </select>\n");
      out.write("          </td>\n");
      out.write("        </tr>\n");
      out.write("      ");
 } 
      out.write("\n");
      out.write("      <tr>\n");
      out.write("         <td>Tags for this profile</td>\n");
      out.write("         <td>\n");
      out.write("             <textarea id=\"tags\" name=\"tags\" title=\"Tags associated with profile\"\n");
      out.write("                       rows=\"2\" style=\"width: 98%;\">");
      out.print( tagsForProfile);
      out.write("</textarea>\n");
      out.write("         </td>\n");
      out.write("       </tr>\n");
      out.write("    </tbody>\n");
      out.write("  </table>\n");
      out.write("  ");
 if (benchmarks.length == 1) { 
      out.write("\n");
      out.write("      <input type=\"hidden\" name=\"benchmark\" value=\"");
      out.print(benchmark );
      out.write("\"></input>\n");
      out.write("  ");
 } 
      out.write("\n");
      out.write("  <br>\n");
      out.write("  <br>\n");
      out.write("  <center><input type=\"submit\" value=\"Select\">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<input type=\"reset\"></center>\n");
      out.write("</form>\n");
      out.write("\n");
          }
        }

      out.write("\n");
      out.write("\n");
      out.write("</body>\n");
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
