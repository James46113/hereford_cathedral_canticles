const updateCanticles = () => {
    fetch('canticles.json')
        .then(resposne => resposne.json())
        .then(data => {
            const table = document.getElementById('canticles-table');
            while (table.rows.length > 1) {
                table.deleteRow(1);
            }
            data.forEach(service => {
                const row = document.createElement('tr');
                const dateObj = new Date(service.date);
                const formattedDate = `${dateObj.getDate()} ${dateObj.toLocaleString('en-US', { month: 'short' })}`;
                row.innerHTML = `<td>${formattedDate}</td><td>${service.canticles}</td><td>${service.composer}</td><td>${service.type}</td>`;
                table.appendChild(row);
            });
            const fillRows = () => {
                const table = document.getElementById('canticles-table');
                const rowHeight = table.rows[0].offsetHeight || 24;
                const tableRect = table.getBoundingClientRect();
                const visibleRows = Math.floor(window.innerHeight / rowHeight)-1;
                while (table.rows.length < visibleRows) {
                    const emptyRow = document.createElement('tr');
                    emptyRow.innerHTML = '<td colspan="4">&nbsp;</td>';
                    table.appendChild(emptyRow);
                }
            };
            fillRows();
            window.addEventListener('resize', fillRows);

            const dateTimeRow = document.createElement('tr');
            const now = new Date();
            const dayOfWeek = now.toLocaleString('en-US', { weekday: 'long' });
            const date = `${now.getDate()} ${now.toLocaleString('en-US', { month: 'long' })}`;
            dateTimeRow.innerHTML = `<td colspan="4">
            <div id="datetime-row">
                <span id="date">${date}</span>
                <span id="time">${now.toLocaleTimeString()}</span>
                <span id="dayOfWeek">${dayOfWeek}</span>
            </div>
            </td>`;
            table.appendChild(dateTimeRow);
        })
        .catch(error => {
            console.error('Error fetching data.')
        })
}

updateCanticles()
setInterval(updateCanticles, 1000)