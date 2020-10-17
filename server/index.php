<?php

//file definitions
$filePath = "data.json";
$encodedSignal = "encoded";

//open file
$file = fopen($filePath, "r") or die("Unable to open file!");
$fileSize = filesize($filePath);
if ($fileSize > 0) {
  //get content of file
  $content = fread($file, $fileSize);
  fclose($file);
  //if file is encrypted, decrypt
  if (strpos($content, $encodedSignal) === 0) {
    $content = substr($content, strlen($encodedSignal));
    $content = base64_decode($content);
  }
  //decode file into json
  $json = json_decode($content);

  //POST handler (for creating new notifications)
  if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $title = $_REQUEST["title"];
    $content = $_REQUEST["content"];
    $iconData = $_REQUEST["iconData"];
    $recieverUUID = $_REQUEST["recieverUUID"];
    $sender = $_REQUEST["sender"];

    //$struct = new Notification(base64_encode($title), base64_encode($content), base64_encode($iconData), base64_encode($recieverUUID), base64_encode($sender), base64_encode(0));
    //save encoded data into struct
    $struct = new stdClass();
    $struct->title = base64_encode($title);
    $struct->content = base64_encode($content);
    $struct->iconData = base64_encode($iconData);
    $struct->recieverUUID = base64_encode($recieverUUID);
    $struct->sender = base64_encode($sender);
    $struct->id = base64_encode(0);

    //add struct to array
    array_push($json->data->unhandledNotifications, $struct);
    echo "Successfully added Notification";

    //save file
    $content = json_encode($json);
    //$encoded = base64_encode($content);
    //$newFileContent = $encodedSignal . $encoded;
    $file = fopen($filePath, "w") or die("Unable to open file!");
    fwrite($file, $content);
    fclose($file);
    header("Location: /create.html");
    die();
  } else {
    $encodedPCName = $_GET["pcname"];
    if ($encodedPCName === "") {
      echo $json;
      echo "true";
    } else {
      $pcName = $encodedPCName;
    
      $uuids = $json->data->pcs;
      $uuid = "";
      foreach ($uuids as &$pc) {
        if ($pc->name === $pcName) {
          $uuid = $pc->uuid;
        }
      }
      $notifications = array();
      $unhandledNotifications = $json->data->unhandledNotifications;
      $i = 0;
      foreach ($unhandledNotifications as &$notification) {

        if (base64_decode($notification->recieverUUID) === $uuid) {
          $notifications[] = $notification;
          unset($json->data->unhandledNotifications[$i]);
        }
        $i++;
      }
      echo json_encode($notifications);


      $content = json_encode($json);
      //$encoded = base64_encode($content);
      //$newFileContent = $encodedSignal . $encoded;
      $file = fopen($filePath, "w") or die("Unable to open file!");
      fwrite($file, $content);
      fclose($file);
    }
  }
}
