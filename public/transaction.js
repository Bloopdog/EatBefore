var user_id = sessionStorage.getItem("user_id");

$(async() => {
    var serviceURL = "http://127.0.0.1:5003/transaction/user/" + user_id;

    try {
        const response = 
            await fetch(
                serviceURL, {method: 'GET'}
            );
        const result = await response.json();
        if (response.status === 200) {
            var transactions = result.data.transactions;
            if (transactions.length > 0){
                var rows = "";
                var rowNo = 0;
                for (const transaction of transactions) {
                    rowNo = rowNo + 1;
                    eachRow = `
                        <tr>
                            <th scope="row">${rowNo}</th>
                            <td>${transaction.transaction_date}</td>
                            <td>${transaction.transaction_type}</td>
                            <td>${transaction.transaction_amount}</td>
                        </tr>
                    `;
                    rows += eachRow;
                }
                $('#transaction_rows').append(rows);
            } else {
                $('#transactions').html('<p>You do not have any transactions</p>')
            }
        } else if (response.status == 404) {
            showError(result.message);
        } else {
            throw response.status;
        }
    } catch(error) {
        showError('There is a problem retrieving transaction data, please try again later.<br />' + error);
    }
});