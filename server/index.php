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
    $iconPath = $_POST["iconPath"];
    $recieverUUID = $_POST["recieverUUID"];
    $sender = $_POST["sender"];

    $struct;
    $struct->title = $title;
    $struct->content = $content;
    $struct->iconPath = $iconPath;
    $struct->recieverUUID = $recieverUUID;
    $struct->sender = $sender;
    $struct->id = 0;

    array_push($json->data->unhandledNotifications, $struct);
    echo "Successfully addedd Notification";
  }else{
    $pcName = base64_decode($_GET["pcname"]);
    $uuids = $json->data->pcs;
    $uuid = "";
    foreach($uuids as &$pc){
      if($pc->name === $pcName){
        $uuid = $pc->uuid;
      }
    }
    $notifications = [];
    $unhandledNotifications = $json->data->unhandledNotifications;
    foreach($unhandledNotifications as &$notification){
      if($notification->recieverUUID === $uuid){
        array_push($notifications, $notification);
      }
    }
    echo json_encode($notifications);
  }

  $content = json_encode($json);
  $encoded = base64_encode($content);
  $newFileContent = $encodedSignal . $encoded;
  $file = fopen($filePath, "w") or die("Unable to open file!");
  fwrite($file, $newFileContent);
  fclose($file);
}
?>