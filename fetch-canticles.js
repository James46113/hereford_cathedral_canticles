fetch('canticles.json')
.then(resposne => resposne.json())
.then(data => {
    console.log(data)
})
.catch(error => {
    console.error('Error fetching data.')
})