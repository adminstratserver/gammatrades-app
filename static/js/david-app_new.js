

/*
			KEY COMPONENTS:
			"activeItem" = null until an edit button is clicked. Will contain object of item we are editing
			"list_snapshot" = Will contain previous state of list. Used for removing extra rows on list update

			PROCESS:
			1 - Fetch Data and build rows "buildList()"
			2 - Create Item on form submit
			3 - Edit Item click - Prefill form and change submit URL
			4 - Delete Item - Send item id to delete URL
			5 - Cross out completed task - Event handle updated item

			NOTES:
			-- Add event handlers to "edit", "delete", "title"
			-- Render with strike through items completed
			-- Remove extra data on re-render
			-- CSRF Token
		*/

function getCookie(name) {
		    var cookieValue = null;
		    if (document.cookie && document.cookie !== '') {
		        var cookies = document.cookie.split(';');
		        for (var i = 0; i < cookies.length; i++) {
		            var cookie = cookies[i].trim();
		            // Does this cookie string begin with the name we want?
		            if (cookie.substring(0, name.length + 1) === (name + '=')) {
		                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
		                break;
		            }
		        }
		    }
		    return cookieValue;
	}
		var csrftoken = getCookie('csrftoken');

		var activeItem = null
		var list_snapshot = []


buildList()

		// This function is responsible for fetching data from back-end and output data into the document
		function buildList(){
			var wrapper = document.getElementById('list-wrapper')
			//wrapper.innerHTML = ''

			//fetching data from backend
			var url = 'http://127.0.0.1:8000/mydocuments/task-list/'
			var urledit = 'http://127.0.0.1:8000/mydocuments/edit/'

			fetch(url)
			.then((resp) => resp.json())
			.then(function(data){
				console.log('Data001:', data)  //display at console
            // render the data into the document
				var list = data
				for (var i in list){

          // check for exceptions
					try{
						document.getElementById(`data-row-${i}`).remove()
					}catch(err){

					}


          // render title

					var title = `<span class="title">${list[i].title}</span>`
					var type = `<span class="type">${list[i].type}</span>`
					var list_date = `<span class="list_date">${list[i].list_date.substring(0,10)}</span>`
                    var check01

                    /*
                    if (list[i].is_published == true){
						title = `<strike class="title">${list[i].title}</strike>`
					}*/


                    //console.log('** item =',list[i].title, list[i].is_published );
					if (list[i].is_published == true){

						check01 = `<input type="checkbox" name="name-${i}" id="${i}" checked><span><label for="${i}"></label></span>`
                    }
                    else{
                        check01 = `<input type="checkbox" name="name-${i}" id="${i}"><span><label for="${i}"></label></span>`
                    }

                    // console.log('item =',i,list[i].is_published);

					// render individual items
					var item = `
						<div id="data-row-${i}" class="task-wrapper flex-wrapper">


                            <!-- display title -->
							<div style="flex:7">${title}</div>

                            <!-- display type -->
							<div style="flex:6">${type}</div>

                            <!-- display list_date -->
							<div style="flex:5">${list_date}</div>

                            <!-- display switch -->
							<div id="switch-row-${i}" style="flex:3">
							    <div class="switch-button switch-button-xs">
							        ${check01}
                                 </div>
							</div>

							<div style="flex:2">
							    <!-- <a href="${urledit}${list[i].id}" class="badge badge-pill badge-success">Edit</a>  -->
                                    <a href="${urledit}${list[i].id}" class="btn btn-sm btn-outline-dark edit">Edit</a>
							</div>
							<div style="flex:1">
								<button class="btn btn-sm btn-outline-dark delete">Delete</button>
							</div>
						</div>
					`
					wrapper.innerHTML += item
				}


if (list_snapshot.length > list.length){
					for (var i = list.length; i < list_snapshot.length; i++){
						document.getElementById(`data-row-${i}`).remove()
					}
				}

				list_snapshot = list


				for (var i in list){
					var deleteBtn = document.getElementsByClassName('btn btn-sm btn-outline-dark delete')[i]
					var publishSwitch = document.getElementById(`switch-row-${i}`)
					var title = document.getElementsByClassName('title')[i]

					deleteBtn.addEventListener('click', (function(item){
						return function(){
							deleteItem(item)
						}
					})(list[i]))

					publishSwitch.addEventListener('click', (function(item){
						return function(){
							changePublishItem(item)
						}
					})(list[i]))

					title.addEventListener('click', (function(item){
						return function(){
							clickTitleItem(item)
						}
					})(list[i]))


				}

function deleteItem(item){
			console.log('Delete clicked item =', item)

			fetch(`http://127.0.0.1:8000/mydocuments/task-delete/${item.id}/`,
			{
				method:'DELETE',
				headers:{
					'Content-type':'application/json',
					'X-CSRFToken':csrftoken,
				}
			}).then((response) => {
				buildList()
			})
}

function clickTitleItem(item){
			console.log('clicked item =', item.is_published)
		}



function changePublishItem(item){
            //console.log('item              =>', item)
			console.log('1. item.id           =>', item.id)
			console.log('2. item.is_published =>', item.is_published)

            var new_ispublished = !item.is_published
			//item.is_published = !item.is_published
			console.log('3. new_ispublished =>', new_ispublished)




			fetch(`http://127.0.0.1:8000/mydocuments/task-update/${item.id}/`,
			{
				method:'POST',
				headers:{
					'Content-type':'application/json',
					'X-CSRFToken':csrftoken,
				},
				body:JSON.stringify({'title':item.title, 'is_published':new_ispublished})
			}).then((response) => {
				buildList()
			})



		}

})
}