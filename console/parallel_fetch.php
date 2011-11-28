<?php

header('Content-type:text/html; charset=UTF-8');


// アクセス先URL
$baseurl = 'http://www.xxx.zz/';

// アクセス先コンテンツ
$script = 'contents.php';

// GET変数
$argv = 'date';


// 同時アクセス数
$con_num = 50;

// 実行ループ回数
$loop_num = 10;

// 待ち時間 (マイクロ秒 1000000=1秒)
$sleep = 500000; //0.5秒


// GET指定が無い場合はNone
if ( !$_GET['id'] ) { $_GET['id'] = 'None'; }


// $_GET 送信用のIDナンバー
$cur_num = 1;

// ループ開始
for ( $i = 0; $i < $loop_num; $i++ ){
    //並列実行のリストを作成
    $url_list = array();
    for ( $j = 0; $j < $con_num ; $j++ ){
        $url_list[$j] = $baseurl . $script . '?id='. $_GET['id'] 
                                                   .'&'.  $argv . '=' . $cur_num++ ;
    }

    //開始時間取得
    $time = time();

    //実行
    $res = fetch_multi_url($url_list);

    //結果出力
    echo '実行結果:<pre>';
    print_r($res);
    echo '</pre>';

    //実行時間
    echo '--<br />time:'.(time() - $time).' sec <br />';
 
    usleep($sleep);
}

echo "Done!!!!!";
exit;



/**
* 複数URLを同時に取得する
*
* @param array $url_list URLの配列
* @param int $timeout タイムアウト秒数 0だと無制限
* @return array 取得したソースコードの配列
*/
function fetch_multi_url ($url_list, $timeout=0 ) {
    $mh = curl_multi_init();


    foreach ($url_list as $i => $url) {
        $conn[$i] = curl_init($url);
        curl_setopt($conn[$i],CURLOPT_RETURNTRANSFER,1);
        curl_setopt($conn[$i],CURLOPT_FAILONERROR,1);
        curl_setopt($conn[$i],CURLOPT_FOLLOWLOCATION,1);
        curl_setopt($conn[$i],CURLOPT_MAXREDIRS,3);

        //SSL証明書を無視
        curl_setopt($conn[$i],CURLOPT_SSL_VERIFYPEER,false);
        curl_setopt($conn[$i],CURLOPT_SSL_VERIFYHOST,false);

        //タイムアウト
        if ($timeout){
            curl_setopt($conn[$i],CURLOPT_TIMEOUT,$timeout);
        }

        curl_multi_add_handle($mh,$conn[$i]);
    }

    //URLを取得
    //すべて取得するまでループ
    $active = null;
    do {
        $mrc = curl_multi_exec($mh,$active);
    } while ($mrc == CURLM_CALL_MULTI_PERFORM);

    while ($active and $mrc == CURLM_OK) {
        if (curl_multi_select($mh) != -1) {
            do {
                $mrc = curl_multi_exec($mh,$active);
            } while ($mrc == CURLM_CALL_MULTI_PERFORM);
        }
    }

    if ($mrc != CURLM_OK) {
        echo '読み込みエラーが発生しました:'.$mrc;
    }

    //ソースコードを取得
    $res = array();
    foreach ($url_list as $i => $url) {
        if (($err = curl_error($conn[$i])) == '') {
            $res[$i] = curl_multi_getcontent($conn[$i]);
        } else {
            echo '取得に失敗しました:'.$url_list[$i].'<br />';
        }
        curl_multi_remove_handle($mh,$conn[$i]);
        curl_close($conn[$i]);
    }
    curl_multi_close($mh);

    return $res;
}

# */

?>