<?php
// 読み込むディレクトリ名
$dir = "./";
$sizedir = "../dirsize/";
$files = scandir($dir);
uksort($files, 'strnatcasesort');
$data = array();


// txtファイルから内容を取得
foreach ($files as $value){
	if (ereg("\.txt$", $value)){
		$data[$value] = file($value) or die("ファイルが見つかりません。");
	}
}


echo <<< EOF
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<html lang="ja-JP">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<link rel="stylesheet" type="text/css" href="css.css">
<title>Applogic Server Info</title>
</head>
<body>
<h1>サーバー情報</h1>
<ul>
  <li><a href="./atlantic.php">atlantic.php</a>
  <li><a href="./pacific.php">pacific.php</a>
  <li><a href="./unclassified.php">unclassified.php</a>
</ul>
<table summary="サーバー情報"><tbody>
<tr id="title"><th colspan="6" class="summary">サマリー</th><th colspan="4" class="shdd">HDD</th><th colspan="7" class="sversion">バージョン</th><th colspan="6" class="srun">自動起動</th><th class="other">その他</th></tr>
<tr id="title2"><th class="name">サーバー</th><th class="ip">IPアドレス</th><th class="cpu">CPU</th><th class="memory">メモリ</th><th class="fmemory">空きメモリ</th><th class="fmemory2">空きメモリ+</th><th class="hdd">HDD</th><th class="uhdd">HDD使用量</th><th class="phdd">HDD使用率</th><th class="ahdd">空きHDD</th>
<th class="apache">Apache</th><th class="apachey">Apache (yum)</th><th class="php">PHP</th><th class="phpe">eAccelerator</th><th class="pgsql">PostgreSQL</th><th class="mysql">MySQL</th><th class="zabbix">ZABBIX</th>
<th class="rapache">Apache</th><th class="rapachey">Apache (yum)</th><th class="rpgsql">PostgreSQL</th><th class="rmysql">MySQL</th><th class="rvsftpd">vsftpd</th><th class="rzabbix">ZABBIX</th><th class="cdate">ディレクトリ構造更新日</th></tr>

EOF;


$time = mktime();

foreach ( $data as $key=>$value){
	if ( $time  - filemtime($key) > 259200 ){
		continue;	// 更新が3日以上前ならスキップ
	}
	$summary = explode("\t", $value[0]);
	$version = explode("\t", $value[1]);
	$autorun = explode("\t", $value[2]);
	
	## サマリー・HDD表示部
	$key = str_replace('.txt', '.html', $key);
	echo '<tr><td class="left"><a href="'. $sizedir.$key .'">' . $summary[0] .'</a></td>';
	if ($summary[1] == '-'){ echo '<td class="center false">'; }
	else { echo '<td class="left">'; }
	echo $summary[1] .'</td>';
	
	$num = 2;

	## CPU表示
	while(3 > $num){
		if ($num==2){
			if ($summary[$num] == '-'){echo '<td class="center false">';}
			elseif ($summary[$num] > 4){echo '<td class="center over">';}
			elseif ($summary[$num] > 2){echo '<td class="center high">';}
			elseif ($summary[$num] > 1){echo '<td class="center middle">';}
			else {echo '<td class="center">';}

			echo $summary[$num] . '</td>';
		}		
		$num++ ;
	}
	## 3メモリ・4空きメモリ・5空きメモリ＋・6HDD・7使用量・8使用率・9空きHDD
	while(count($summary) > $num){
		if ($summary[$num] == '-'){echo '<td class="right false">'. $summary[$num] .'</td>';}
		elseif ($num==8){
			if (substr($summary[$num], 0, -1) >= 90){echo '<td class="right over">';}
			elseif (substr($summary[$num], 0, -1) >= 80){echo '<td class="right high">';}
			else {echo '<td class="right">';}
			echo $summary[$num] . '</td>';
		}
		elseif ($num==9){
			$summary[$num] = rtrim($summary[$num]);
			if (substr($summary[$num], -1) == "M"){echo '<td class="right over">';}
			elseif (substr($summary[$num], 0, -1) < 2){echo '<td class="right high">';}
			else {echo '<td class="right">';}
			echo $summary[$num] . '</td>';
		}
		else{echo '<td class="right">'. $summary[$num] .'</td>';}
		$num++;
	}
	
	foreach($version as $val){
		echo '<td class="center">'. $val .'</td>';
	}
	foreach($autorun as $val){
		echo '<td class="center">'. $val .'</td>';
	}

	if(is_file($sizedir.$key)){echo '<td class="center">'. gmdate("m月d日", filemtime($sizedir.$key) + 9 * 3600) .'</td>';}
	else { echo '<td class="center false">-</td>'; }
	echo "</tr>\n";
}

echo '</tbody></table></body></html>';

?>

