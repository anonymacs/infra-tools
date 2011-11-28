<?php
//Pythonの場所
$py = 'ping.py';


// POST部分
$cIP = $_POST['cIP']. '=';
$num = $_POST['num']. '=';
$sec = $_POST['sec']. '=';
$out = $_POST['t_out'];

$argpy = $cIP . $num . $sec . $out;

$py = '/usr/bin/env python ./'. $py .' '. $argpy;

$ping = shell_exec($py);

echo $ping;
