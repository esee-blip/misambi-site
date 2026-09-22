<?php
/* =========================================================================
   Misambi Medical Mission — contact form handler
   1. Set $to below to the inbox that should receive messages.
   2. Create that mailbox in your hosting control panel (cPanel > Email Accounts)
      if it doesn't exist yet.
   ========================================================================= */

$to        = "info@misambimedicalmission.org";          // <-- where messages go
$from      = "no-reply@misambimedicalmission.org";      // must be on your own domain
$site_name = "Misambi Medical Mission website";

$topics = [
  "general"   => "General enquiry",
  "donation"  => "Donation or receipt",
  "volunteer" => "Volunteering",
  "partner"   => "Partnership or sponsorship",
  "camp"      => "Request a medical camp",
];

function back($query) {
  header("Location: contact.html?" . $query . "#form", true, 303);
  exit;
}

if ($_SERVER["REQUEST_METHOD"] !== "POST") {
  header("Location: contact.html", true, 303);
  exit;
}

// Spam trap: bots fill every field, people never see this one
if (!empty($_POST["website"])) {
  back("sent=1");
}

function cut($text, $max) {
  return function_exists("mb_substr") ? mb_substr($text, 0, $max) : substr($text, 0, $max);
}

$clean = function ($value, $max) {
  $value = trim((string)($value ?? ""));
  $value = str_replace(["\r", "\n", "%0a", "%0d"], " ", $value);
  return cut(strip_tags($value), $max);
};

$name    = $clean($_POST["name"] ?? "", 100);
$phone   = $clean($_POST["phone"] ?? "", 30);
$email   = trim((string)($_POST["email"] ?? ""));
$topic   = is_string($_POST["topic"] ?? null) ? $_POST["topic"] : "general";
$message = trim(strip_tags((string)($_POST["message"] ?? "")));
$message = cut($message, 5000);

if ($name === "" || $message === "" || !filter_var($email, FILTER_VALIDATE_EMAIL)) {
  back("error=1");
}
if (!array_key_exists($topic, $topics)) {
  $topic = "general";
}

$subject = "[Website] " . $topics[$topic] . " from " . $name;
$body  = "New message from the $site_name\n";
$body .= "----------------------------------------\n";
$body .= "Name:   $name\n";
$body .= "Email:  $email\n";
$body .= "Phone:  " . ($phone !== "" ? $phone : "-") . "\n";
$body .= "Topic:  " . $topics[$topic] . "\n";
$body .= "----------------------------------------\n\n";
$body .= $message . "\n";

$headers  = "From: $site_name <$from>\r\n";
$headers .= "Reply-To: $name <$email>\r\n";
$headers .= "MIME-Version: 1.0\r\n";
$headers .= "Content-Type: text/plain; charset=UTF-8\r\n";

$ok = @mail($to, "=?UTF-8?B?" . base64_encode($subject) . "?=", $body, $headers, "-f" . $from);

back($ok ? "sent=1" : "error=1");
