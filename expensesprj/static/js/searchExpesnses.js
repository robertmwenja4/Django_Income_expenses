const searchExpenses = document.querySelector('#searchField');
const tableOutput = document.querySelector('.table-output');
const appTable = document.querySelector('.app-table');
const paginationContainer = document.querySelector('.pagination-container');
tableOutput.style.display = "none";
const tbody = document.querySelector('.table-body')

searchExpenses.addEventListener('keyup', (e)=>{
    const searchVal = e.target.value;
    console.log(searchVal);
    if (searchVal.trim().length > 0) {
        appTable.style.display = "none";
        tbody.innerHTML = '';
        fetch("/search-expenses",
            {
                body: JSON.stringify({searchText: searchVal}),
                method: 'POST', 
            }
        ).then((res)=> res.json())
        .then((data)=>{
            console.log(data);
            paginationContainer.style.display = "none";
            appTable.style.display = "none";
            
            tableOutput.style.display = "block";
            if(data.length === 0){
                tableOutput.innerHTML = "No data Found";
                paginationContainer.style.display = "none";
            }else{
                data.forEach(element => {
                    tbody.innerHTML += `
                    <tr>
                        <td>${element.amount}</td>
                        <td>${element.category}</td>
                        <td>${element.description}</td>
                        <td>${element.date}</td>
                        <td>
                            <a class="btn btn-secondary" href="/edit-expense/${element.id}">
                                Edit
                            </a>
                        </td>
                    </tr>
                    `;
                });
            }
            
        })
    }else{
        appTable.style.display = "block";
        paginationContainer.style.display = "block";
        tableOutput.style.display = "none";

    }
});