<?php
// 読み込むディレクトリ名
$dir = "./";
$files = scandir($dir);
$link = array();

foreach ($files as $key=>$value){
	if (ereg("\.html$", "$value")){
		$value = mb_convert_encoding($value, "UTF-8", "SJIS, EUC-JP, JIS, ASCII");
		$link[$value] = gmdate("m/d (D)  (H:i:s)", filemtime($dir.$value) + 9 * 3600);
	}
}

ksort($link);

echo ' <html>
<head>
<link rel="stylesheet" type="text/css" href="css.css">
<title>Applogic Server Info</title>
</head>
<body>
<h1>サーバー情報</h1>
<body>';
echo '<table><tbody>';

foreach ( $link as $name=>$date){
	echo '<tr><td><a href='.$name.'>'.$name.'</a></td><td> '.$date."</td></tr>\n";
}
echo '</tbody></table></body></html>';

?>
