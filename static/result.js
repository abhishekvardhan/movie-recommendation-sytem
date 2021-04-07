
document.getElementById("btn0").onclick = function () { b0() };
document.getElementById("btn1").onclick = function () { b1() };
document.getElementById("btn2").onclick = function () { b2() };
document.getElementById("btn3").onclick = function () { b3() };
document.getElementById("btn4").onclick = function () { b4() };
document.getElementById("btn5").onclick = function () { b5() };
document.getElementById("btn6").onclick = function () { b6() };
document.getElementById("btn7").onclick = function () { b7() };
document.getElementById("btn8").onclick = function () { b8() };
document.getElementById("btn9").onclick = function () { b9() };
document.getElementById("cst1").onclick = function () { m1() };
document.getElementById("cst2").onclick = function () { m2() };
document.getElementById("cst3").onclick = function () { m3() };
document.getElementById("cst4").onclick = function () { m4() };
document.getElementById("cst5").onclick = function () { m5() };
document.getElementById("cst6").onclick = function () { m6() };
function b0() {
    {
        var d = '{{data['d3'][l[0]]['title']}}';
        document.getElementById("movie_name").value = d;
        document.getElementById("search").click();
    }
}
function b1() {
    {
        var d = '{{data['d3'][l[1]]['title']}}';
        document.getElementById("movie_name").value = d;
        document.getElementById("search").click();
    }
}
function b2() {
    {
        var d = '{{data['d3'][l[2]]['title']}}';
        document.getElementById("movie_name").value = d;
        document.getElementById("search").click();
    }
}
function b3() {
    {
        var d = '{{data['d3'][l[3]]['title']}}';
        document.getElementById("movie_name").value = d;
        document.getElementById("search").click();
    }
}
function b4() {
    {
        var d = '{{data['d3'][l[4]]['title']}}';
        document.getElementById("movie_name").value = d;
        document.getElementById("search").click();
    }
}
function b5() {
    {
        var d = '{{data['d3'][l[5]]['title']}}';
        document.getElementById("movie_name").value = d;
        document.getElementById("search").click();
    }
}
function b6() {
    {
        var d = '{{data['d3'][l[6]]['title']}}';
        document.getElementById("movie_name").value = d;
        document.getElementById("search").click();
    }
}
function b7() {
    {
        var d = '{{data['d3'][l[7]]['title']}}';
        document.getElementById("movie_name").value = d;
        document.getElementById("search").click();
    }
}
function b8() {
    {
        var d = '{{data['d3'][l[8]]['title']}}';
        document.getElementById("movie_name").value = d;
        document.getElementById("search").click();
    }
}
function b9() {
    {
        var d = '{{data['d3'][l[9]]['title']}}';
        document.getElementById("movie_name").value = d;
        document.getElementById("search").click();
    }
}
function m1() {
    document.getElementById("cname").innerHTML = '{{data['d2'][0]['name']}}';
    document.getElementById("birth").innerHTML = '{{data['d2'][0]['dob']}}';
    document.getElementById("gender").innerHTML = '{{data['d2'][0]['gender']}}';
    document.getElementById("cstdesc").innerHTML = '{{data['d2'][0]['bio']}}';
    document.getElementById("cast_phot").src = '{{ url_for('static',filename=data['d2'][0]['poster_p'])}}';
    document.getElementById("modal01").style.display = 'block';
}
function m2() {
    document.getElementById("cname").innerHTML = '{{data['d2'][1]['name']}}';
    document.getElementById("birth").innerHTML = '{{data['d2'][1]['dob']}}';
    document.getElementById("gender").innerHTML = '{{data['d2'][1]['gender']}}';
    document.getElementById("cstdesc").innerHTML = '{{data['d2'][1]['bio']}}';
    document.getElementById("cast_phot").src = '{{ url_for('static',filename=data['d2'][1]['poster_p'])}}';
    document.getElementById("modal01").style.display = 'block';
}
function m3() {
    document.getElementById("cname").innerHTML = '{{data['d2'][2]['name']}}';
    document.getElementById("birth").innerHTML = '{{data['d2'][2]['dob']}}';
    document.getElementById("gender").innerHTML = '{{data['d2'][2]['gender']}}';
    document.getElementById("cstdesc").innerHTML = '{{data['d2'][2]['bio']}}';
    document.getElementById("cast_phot").src = '{{ url_for('static',filename=data['d2'][2]['poster_p'])}}';
    document.getElementById("modal01").style.display = 'block';
}
function m4() {
    document.getElementById("cname").innerHTML = '{{data['d2'][3]['name']}}';
    document.getElementById("birth").innerHTML = '{{data['d2'][3]['dob']}}';
    document.getElementById("gender").innerHTML = '{{data['d2'][3]['gender']}}';
    document.getElementById("cstdesc").innerHTML = '{{data['d2'][3]['bio']}}';
    document.getElementById("cast_phot").src = '{{ url_for('static',filename=data['d2'][3]['poster_p'])}}';
    document.getElementById("modal01").style.display = 'block';
}
function m5() {
    document.getElementById("cname").innerHTML = '{{data['d2'][4]['name']}}';
    document.getElementById("birth").innerHTML = '{{data['d2'][4]['dob']}}';
    document.getElementById("gender").innerHTML = '{{data['d2'][4]['gender']}}';
    document.getElementById("cstdesc").innerHTML = '{{data['d2'][4]['bio']}}';
    document.getElementById("cast_phot").src = '{{ url_for('static',filename=data['d2'][4]['poster_p'])}}';
    document.getElementById("modal01").style.display = 'block';
}
function m6() {
    document.getElementById("cname").innerHTML = '{{data['d2'][5]['name']}}';
    document.getElementById("birth").innerHTML = "{{data['d2'][5]['dob']}}";
    document.getElementById("gender").innerHTML = '{{data['d2'][5]['gender']}}';
    document.getElementById("cstdesc").innerHTML = "{{data['d2'][5]['bio']}}";
    document.getElementById("cast_phot").src = "{{ url_for('static',filename=data['d2'][5]['poster_p'])}}";
    document.getElementById("modal01").style.display = 'block';
}
