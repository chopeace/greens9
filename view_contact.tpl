<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<title>Contact List: {{old[1]}} {{old[2]}}</title>
<link rel="stylesheet" href="/contact/static/style.css" type="text/css" />
</head>
<body>
<h1>Contact List: {{old[1]}} {{old[2]}}</h1>

<dl class="display">
<dt>First name:</dt><dd>
<div class="field">{{old[1]}} </div>
</dd>
<dt>Last name:</dt><dd>
<div class="field">{{old[2]}}</div>
</dd>
<dt>Email:</dt><dd>
<div class="field"><span class="empty">{{old[3]}}</span></div>
</dd>
<dt>Phone Number:</dt><dd>
<div class="field">{{old[4]}}</div>
</dd>
<dt>Notes:</dt><dd>
<div class="field">{{old[5]}}</div>
</dd>
</dl>

<p><a href="/peace/exer9">List of people</a>
| <a href="/peace/exer9/edit/{{old[0]}}">Edit contact</a></p>


</body>
</html>
