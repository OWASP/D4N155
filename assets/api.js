const add = value => {
 let block = document.querySelector("#wrapper");
 let li = document.createElement("textarea");
 li.appendChild(document.createTextNode(value));
 li.setAttribute("onclick", "copy(this)");
	li.classList.add('animated', 'fadeInUp')
 block.appendChild(li);
};

const showNumbers = value => {
 let result = document.querySelector(".result");
 result.innerText = `Results: ${value.result.length} but have more :(`;
};

const show = response => {
 response.result.data.map(add);
 showNumbers(response);
 return false;
};

const search = term => {
 fetch(`https://d4n155.herokuapp.com/domain/600?url=${term}`)
  .then(x => {
   return x.json();
  })
  .then(response => {
   return show(response);
  });
};

const copy = x => {
 x.select();
 document.execCommand("copy");
};

