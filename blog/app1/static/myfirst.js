let data1, data2, data3; // Declare the variables in the global scope

async function fetchData(domain) {
  var url = `https://newsdata.io/api/1/news?apikey=pub_29082b9011b701885fb8d81d47f254bf12744&q=${domain}`;
  var req = new Request(url);

  try {
    const response = await fetch(req);
    const data = await response.json();
    const new2 = data.results;
    
    return new2;
  } catch (error) {
    console.error(error);
  }
}

async function fetchNewsData() {
  const domain1 = "technology";
  const domain2 = "sports";
  const domain3 = "Politics";

  try {
    [data1, data2, data3] = await Promise.all([
      fetchData(domain1),
      fetchData(domain2),
      fetchData(domain3),
    ]);
    console.log('Data for technology:', data1);
    console.log('Data for sports:', data2);
    console.log('Data for politics:', data3);
    const x = document.getElementsByClassName("tech");
    const y =  document.getElementsByClassName("sports");
    const z = document.getElementsByClassName("politics");
    
    
    for (let i = 0; i < Math.min(4, data1.length); i++) {
      const techElement = x[i];
      const sportselement = y[i]
      const politicelement = z[i]
      const imaget = techElement.querySelector('.imagetech');
      const techtitle1 = techElement.querySelector('.techtitle');
      const anchor = techElement.querySelector('.techlink');
      const imaget2 = sportselement.querySelector('.sportimage');
      const sporttitle1 = sportselement.querySelector('.sportstitle');
      const sportanchor = sportselement.querySelector('.sportslink')
      const imaget3 = politicelement.querySelector('.politicsimage');
      const politicstitle1 = politicelement.querySelector('.politicstitle');
      const politicsanchor = politicelement.querySelector('.politicslink')
      if (imaget) {
        if(data1[i].image_url != null){
        imaget.src = data1[i].image_url;
        }else{
          imaget.src = "/static/techblog.jpg"
        }
      }
      if (imaget2) {
        if(data2[i].image_url != null){
        imaget2.src = data2[i].image_url;
        }else{
          imaget2.src = "/static/techblog.jpg"
        }
      }
      if (imaget3) {
        if(data3[i].image_url != null){
        imaget3.src = data3[i].image_url;
        }else{
          imaget3.src = "/static/techblog.jpg"
        }
      }
      if (techtitle1) {
        techtitle1.innerHTML = data1[i].title;
      }
      if (sporttitle1) {
        sporttitle1.innerHTML = data2[i].title;
      }
      if (politicstitle1) {
        politicstitle1.innerHTML = data3[i].title;
      }
      if (anchor){
        anchor.innerHTML = "Click on the Link for full Story"
        anchor.addEventListener("click", function () {
          
          localStorage.setItem("newsDetails", JSON.stringify(data1[i]));
      
          //console.log(newsUrl)
          window.location.href = newsUrl;
          
        })

      }
      if (sportanchor){
        sportanchor.innerHTML = "Click on the Link for full Story"
        sportanchor.addEventListener("click", function () {
          
          localStorage.setItem("newsDetails1", JSON.stringify(data2[i]));
      
          //console.log(newsUrl)
          window.location.href = newsUrl1;
          
        })
        

      }
      if (politicsanchor){
        politicsanchor.innerHTML = "Click on the Link for full Story"
        
        politicsanchor.addEventListener("click", function () {
          
          localStorage.setItem("newsDetails2", JSON.stringify(data3[i]));
      
          //console.log(newsUrl)
          window.location.href = newsUrl2;
          
        })

      }
    }

  }catch (error) {
    console.log(error);
  }
}

fetchNewsData();

function myfunction() {
  alert('alerted');
}

// You can access data1, data2, and data3 here, but they will only be available after fetchNewsData() has completed.
