<?php
require './sss.php';
require './ip.php';
?>
<!DOCTYPE html>
<html>

<head>
	<meta charset="utf-8">
	<meta http-equiv="X-UA-Compatible" content="IE=edge">
	<title>哦</title>
	<meta name="description" content="">
	<meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
	<meta name="robots" content="all,follow">
	<!-- Bootstrap CSS-->
	<link href="https://cdn.bootcss.com/twitter-bootstrap/4.2.1/css/bootstrap.min.css" rel="stylesheet">
	<link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Poppins:300,400,700">
	<link rel="stylesheet" href="css/style.default.css" id="theme-stylesheet">
</head>

<body>
	<div class="page login-page">
		<div class="container d-flex align-items-center">
			<div class="form-holder has-shadow">
				<div class="row">
					<!-- Logo & Information Panel-->
					<div class="col-lg-6">
						<div class="info d-flex align-items-center">
							<div class="content">
								<div class="logo">
									<h1>自动每日一报提交</h1>
									
								</div>
								
							</div>
						</div>
					</div>
					<!-- Form Panel    -->
					<div class="col-lg-6 bg-white">
						<div class="form d-flex align-items-center">
							<div class="content">
							    <!--<img src="fk.png"></img>-->
								<?php
								$servername = "localhost";
								$uname = "";//账号
								$pad = "";//密码
								$dbname = "";//表
								error_reporting(E_ALL ^ E_DEPRECATED);
								$conn = new mysqli($servername, $uname, $pad,$dbname);
								if (!$conn) {
									die("Connection failed: " . mysqli_connect_error());
								}
								$username=$_POST["registerUsername"];
								$password=$_POST["registerPassword"];
								$email=$_POST["registeremail"];
								$username=addslashes($username);
								$password=addslashes($password);
								$email=addslashes($email);
								$ip=getip();
								$encryptObj = new MagicCrypt();//不加密就不需要这个
								$password = $encryptObj->encrypt($password);//加密结果
								$sql = "INSERT INTO user (username, password,email,ip) VALUES ('$username','$password','$email','$ip')";
								if (mysqli_query($conn, $sql)) {
									echo "提交成功！！！";
									
								} else {
									echo "提交失败请检查输入！！";
								}
								$conn->close();
								?>
								<small>取消自动每日一报?</small><a href="register.html" class="signup">&nbsp;取消</a>
							</div>
						</div>
					</div>
				</div>
			</div>
		</div>
	</div>
	<!-- JavaScript files-->
	<script src="https://cdn.bootcss.com/jquery/1.11.1/jquery.min.js"></script>
	<script src="https://cdn.bootcss.com/twitter-bootstrap/4.2.1/js/bootstrap.min.js"></script>
	<script>
		
</body>

</html>