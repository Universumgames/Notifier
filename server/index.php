<?php

$filePath = "data.json";
$encodedSignal = "encoded";

$file = fopen($filePath, "r") or die("Unable to open file!");
$fileSize = filesize($filePath);
if($fileSize > 0){
  $content = fread($file, $fileSize);
  fclose($file);
  if(strpos($content, $encodedSignal) === 0) {
    $content = substr($content, strlen($encodedSignal));
    $content = base64_decode($content);
  }
  $json = json_decode($content);

  if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $title = $_POST["title"];
    $content = $_POST["content"];
    $iconData = $_POST["iconData"];
    $recieverUUID = $_POST["recieverUUID"];
    $sender = $_POST["sender"];

    //$struct = new Notification(base64_encode($title), base64_encode($content), base64_encode($iconData), base64_encode($recieverUUID), base64_encode($sender), base64_encode(0));
    $struct = new stdClass();
    $struct->title = base64_encode($title);
    $struct->content = base64_encode($content);
    $struct->iconData = base64_encode($iconData);
    $struct->recieverUUID = base64_encode($recieverUUID);
    $struct->sender = base64_encode($sender);
    $struct->id = base64_encode(0);

    $arr = [];
    array_push($arr, $struct);
    foreach($json->data->unhandledNotifications as $not){
      array_push($arr, $not);
    }

    $json->data->unhandledNotifications = $arr;
    echo "Successfully added Notification";

    //save file
    $content = json_encode($json);
    $encoded = base64_encode($content);
    $newFileContent = $encodedSignal . $encoded;
    $file = fopen($filePath, "w") or die("Unable to open file!");
    fwrite($file, $newFileContent);
    fclose($file);
  }else{
    $pcName = base64_decode($_GET["pcname"]);
    $uuids = $json->data->pcs;
    $uuid = "";
    foreach($uuids as &$pc){
      if($pc->name === $pcName){
        $uuid = $pc->uuid;
      }
    }
    $notifications = array();
    $unhandledNotifications = $json->data->unhandledNotifications;
    $i = 0;
    foreach($unhandledNotifications as &$notification){
      
      if(base64_decode($notification->recieverUUID) === $uuid){
        $notifications[] = $notification;
        unset($json->data->unhandledNotifications[$i]);
      }
      $i++;
    }
    echo json_encode($notifications);


    $content = json_encode($json);
    $encoded = base64_encode($content);
    $newFileContent = $encodedSignal . $encoded;
    $file = fopen($filePath, "w") or die("Unable to open file!");
    fwrite($file, $newFileContent);
    fclose($file);
  }
}
?>