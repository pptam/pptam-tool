function get_element(id) {
    if ( document.getElementById )
        return document.getElementById( id );
    else if ( document.all )
        return eval( "document.all." + id );
    else
        return false;
}
function toggle(id){
    ele = get_element(id);
    if ( ele.style.display != "block" ) {
        ele.style.display = "block"
    } else {
        ele.style.display = "none"
    }
    return true;
}
/* This function color codes the comparison table */
function color_code(id) {    
    table = get_element(id);
    if (table == false) return false;
    var tbody = table.getElementsByTagName('tbody')[0];
    var rows = tbody.getElementsByTagName('tr');
    for (var i = 0; i < rows.length; i++) {
        var cols = rows[i].getElementsByTagName('td');
        if ( cols.length < 3)
            return false;
        var same=1;
        for (var j = 1; j < cols.length - 1; j++) {
            if ( cols[j].innerHTML != cols[j+1].innerHTML)
                same=0;
            break;
        }
        if (same == 0) {
            cols[0].style.color="#FF1A00";
        }
    }
    return true;
}
function hide_similar(id){
    table = get_element(id);
    if (table == false) return false;
    var tbody = table.getElementsByTagName('tbody')[0];
    var rows = tbody.getElementsByTagName('tr');
    for (var i = 0; i < rows.length; i++) {
        var cols = rows[i].getElementsByTagName('td');
        if ( cols.length < 3)
            return false;
        var same=1;
        for (var j = 1; j < cols.length - 1; j++) {
            if ( cols[j].innerHTML != cols[j+1].innerHTML)
                same=0;
            break;
        }
        if (same == 1) {
            rows[i].style.display="none";
        }
    }
    return true;
}
function show_all(id){
    table = get_element(id);
    if (table == false) return false;
    var tbody = table.getElementsByTagName('tbody')[0];
    var rows = tbody.getElementsByTagName('tr');
    for (var i = 0; i < rows.length; i++) {
        rows[i].style.display="";
    }
    return true;
}
