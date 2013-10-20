<?php
include '../cgi/dbutil.php';

$db = DBUtil::connect();

$fname = trim($_POST['fname']);
$lname = trim($_POST['lname']);
$email = trim($_POST['email']);

$password = md5(trim($_POST['password']));

$stmt = $db->stmt_init();
if( $stmt->prepare("SELECT ID FROM users WHERE fname=? AND lname=?") ) {
	$stmt->bind_param('ss', $fname, $lname);
	$stmt->execute();
	$stmt->bind_result($id);
	if( $stmt->fetch() ) {
		if($_FILES['pic']['size'] == 0) {
			$filename = 'anonymous.png';
		}
		else {
			$extension = end(explode(".", $_FILES['pic']['name']));
			$filename = strval($id)."_".$fname."_".$lname.'.'.$extension;
			$uploadfile = '../profilePics/'.$filename;
			
			if (!move_uploaded_file($_FILES['pic']['tmp_name'], $uploadfile)) {
	    		$filename = 'anonymous.png';
	    	}
		}
	
		if( $stmt->prepare("INSERT INTO loginInfo (ID, password, email, photo) VALUES (?, ?, ?, ?)") ) {
			$stmt->bind_param('ssss', $id, $password, $email, $filename);
			$stmt->execute();
			
			session_start();
			$_SESSION["fname"] = $fname;
			$_SESSION["lname"] = $lname;
			$_SESSION["id"] = $id;
			$_SESSION["photo"] = $filename;
			header('Location: ../index.php');
		}
		else {
			echo "<p>There was an error registering your account. Please try again in a few minutes</p>";
		}
	}
	else {
		echo "<p>No records match the information you gave.</p>";
	}
}

$stmt->close();
?>