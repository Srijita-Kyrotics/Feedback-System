let studentCount = 0;

function addRow() {
    studentCount++;
    const tbody = document.getElementById('tableBody');
    const row = document.createElement('tr');
    row.id = `row-${studentCount}`;
    
    row.innerHTML = `
        <td>Student ${studentCount}</td>
        <td><input type="number" class="cat-1 score-input" min="0" max="5" value="5"></td>
        <td><input type="number" class="cat-2 score-input" min="0" max="5" value="5"></td>
        <td><input type="number" class="cat-3 score-input" min="0" max="5" value="5"></td>
        <td><input type="number" class="cat-4 score-input" min="0" max="5" value="5"></td>
        <td><input type="number" class="cat-5 score-input" min="0" max="5" value="5"></td>
        <td><input type="number" class="cat-6 score-input" min="0" max="5" value="5"></td>
        <td><input type="number" class="cat-7 score-input" min="0" max="5" value="5"></td>
        <td><button class="btn btn-add" style="background: rgba(239, 68, 68, 0.1); color: #ef4444; border: 1px solid rgba(239, 68, 68, 0.2);" onclick="removeRow(${studentCount})">×</button></td>
    `;
    
    tbody.appendChild(row);
}

function removeRow(id) {
    const row = document.getElementById(`row-${id}`);
    row.remove();
}

function calculate() {
    const students = document.querySelectorAll('#tableBody tr');
    if (students.length === 0) {
        alert("Please add at least one student.");
        return;
    }

    const n = students.length;
    let categorySums = [0, 0, 0, 0, 0, 0, 0];

    students.forEach(row => {
        for (let i = 1; i <= 7; i++) {
            const val = parseFloat(row.querySelector(`.cat-${i}`).value) || 0;
            categorySums[i-1] += Math.min(5, Math.max(0, val)); // Clamp between 0-5
        }
    });

    let totalAvg = 0;
    categorySums.forEach((sum, index) => {
        const avg = sum / n;
        totalAvg += avg;
        document.getElementById(`avg${index + 1}`).innerText = avg.toFixed(2);
    });

    const percentage = (totalAvg / 35) * 100;

    document.getElementById('totalScore').innerText = totalAvg.toFixed(2);
    document.getElementById('percentage').innerText = percentage.toFixed(2) + '%';
    document.getElementById('resultsGrid').style.display = 'grid';
    
    // Smooth scroll to results
    document.getElementById('resultsGrid').scrollIntoView({ behavior: 'smooth' });
}

// Add first 10 students by default as per request
window.onload = () => {
    for (let i = 0; i < 10; i++) {
        addRow();
    }
};
