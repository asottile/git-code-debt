<!doctype html>
<html>
<head>
  <%block name="css">
    <link rel="stylesheet" type="text/css" href="http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.3/themes/dot-luv/jquery-ui.css">
  </%block>
  <title><%block name="title" /></title>
</head>
<body>
  ${self.body()}
  <%block name="scripts">
    <script src="http://ajax.googleapis.com/ajax/libs/jquery/1.10.2/jquery.js"></script>
    <script src="http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.3/jquery-ui.min.js"></script>
  </%block>
</body>
</html>
