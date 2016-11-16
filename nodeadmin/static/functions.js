/**
 * Created by caterina on 19-10-16.
 */
function confirmDelete(key_id) {
        r = confirm("This will delete all the key shares associated with this public key");
        if(r){
            window.location = "/delete_key/" + key_id
        }
    }
