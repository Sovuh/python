(function(){
    if (window.MyBookmarklet !== undefined){
        myBookmarklet();
    }
    else {
        document.body.appendChild(
            document.createElement('script')
        ).src='=\'https://3f6ad53c.ngrok.io/static/js/bookmarklet?r=' + math.floor(Math.random()*99999999999999999999)
    }
})