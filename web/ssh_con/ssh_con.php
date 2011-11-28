<?php

#====================
# 初期値
#====================
$sship = 'xxx.xxx.xxx.xxx';
$sshuser = 'user';
$sshpass = 'pass';


#====================
# 処理開始
#====================
$com_id = $_POST['com_id'];

if ($com_id == '1'){

	$connection = connect();
	
	$command = '';
	sshcommand($connection, $command);
/*	
	$result = explode("\n", $result);
	print_r( $result );
	$string = '';
	foreach ($result as $value){
		$string .= "<b>".$value."</b> - ";
		$string .= "<br/>\n";
	}
	echo $string;
*/
}

elseif($com_id == '2'){
	$command = $_POST['comtext'];
	$connection = connect();
	sshcommand($connection, $command);

}

else { echo "error!"; }



#====================
# 関数：SSHコネクト
#====================
function connect(){
	global	$sship, $sshuser, $sshpass ;

	$connection = ssh2_connect($sship, 22);
	if ( !ssh2_auth_password($connection, $sshuser, $sshpass) ) {
		die('SSHのユーザー認証に失敗しました');
	}
	echo "SSHで $sship に接続しました<br />\n";
	
	return $connection;

}

function sshcommand($connection, $command){

	$stdio_stream = ssh2_exec($connection, $command);
	// stderrサブストリームを取得する
	$stderr_stream = ssh2_fetch_stream($stdio_stream, SSH2_STREAM_STDERR);
	stream_set_blocking($stdio_stream, true);
	
	
	if ( preg_match( "/[a-zA-Z0-9]/", fread($stdio_stream, 64) )){
		echo "<b>STD Message:</b><br />\n<p class=\"msg\">";
		$std = explode( "\n", fread($stdio_stream, 4096) );
		foreach ($std as $val){ echo $val . "<br />\n"; }
		echo "</p>\n<br />";
	}
    
	if ( preg_match( "/[a-zA-Z0-9]/", fread($stderr_stream, 64) )){
		echo "<b>STD Error:</b><br />\n<p class=\"msg2\">";
		echo fread($stderr_stream, 4096);
		echo "</p>\n<br />";
	}


}
?>