const synonyms = JSON.parse(document.getElementById('synonyms').textContent);
const words = JSON.parse(document.getElementById('words').textContent);

document.oncontextmenu = rightClick;
document.onclick = hideMenu;

//For Hiding the contextMenu
function hideMenu() { 
    document.getElementById("contextMenu").style.display = "none";
}



//Whenever user right click
function rightClick(e) { 
    e.preventDefault(); 

    var Word = e.target.innerText;		// This is our current wrong word, where user right clicked
    
    if(!(Word in words)) return;

    var suggestions = synonyms[words[Word]];	// This is the complete array of wrong words in the paragraph
    

    var list = document.createElement("div"); // Created an 
    list.style.backgroundColor = '#c0cccf';
    list.style.width = '100px';

    

    // Generate a list of all the suggestions 
    for(let j = 0; j < suggestions.length; j++ ){
        const Parent = document.getElementById("contextMenu");
        while(Parent.firstChild){
            Parent.firstChild.remove();
        }

        // Create a li and append suggestion
        var li = document.createElement("li");
        li.innerText = suggestions[j];

        //If user click on suggestion , remove highlight class
        li.addEventListener('click', (ev) => {
            e.target.innerHTML = ev.target.innerHTML;
            e.target.style.backgroundColor = null;
        })

        // Append it to our list 
        list.appendChild(li);
        list.style.listStyleType = "none";
    }
    document.getElementById('contextMenu').appendChild(list);
    console.log(document.getElementById('contextMenu'));
    console.log(document.getElementById('contextMenu').firstChild.childElementCount);

    if (document.getElementById("contextMenu").style.display == "block"){ 
        hideMenu();
    }
    else { 
        var menu = document.getElementById("contextMenu") 
              
        menu.style.display = 'block'; 
        menu.position = "absolute";
        menu.style.left = e.clientX + "px"; 
        menu.style.top = e.clientY + "px"; 
    } 
}
