echo "Choose a tool:"
select opt in "Temp GPG Key" "Upload Logs" "QR Export"; do
  case $opt in
    "Temp GPG Key") ./generate_temp_key.sh ;;
    "Upload Logs") ./upload_encrypted_log.sh ;;
    "QR Export")
      read -p "Enter unlock token: " tok
      ./qr_export_token.sh "$tok"
      ;;
    *) echo "Invalid" ;;
  esac
  break
done
