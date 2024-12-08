// Pagination and table management for employees
class EmployeeTable {
    constructor() {
        this.employees = []; // Initially empty, to be populated with fetched data
        this.currentPage = 1;
        this.rowsPerPage = 10;
        this.totalPages = 1; // Will be updated after data is fetched

        this.tableBody = document.getElementById('employeeTableBody');
        this.pageNumbers = document.getElementById('pageNumbers');
        this.prevButton = document.getElementById('prevPage');
        this.nextButton = document.getElementById('nextPage');
        this.searchInput = document.getElementById('employeeSearch');

        this.filteredEmployees = [...this.employees];

        this.initialize();
    }

    initialize() {
        this.fetchEmployees(); // Fetch the employee data from the backend
        this.setupEventListeners();
    }

    async fetchEmployees() {
        try {
            // Fetch employee data from the backend API
            const response = await fetch('http://localhost:3000/api/employees');
            
            // Check if the response is ok (status code 200)
            if (!response.ok) {
                throw new Error('Failed to fetch employee data');
            }

            this.employees = await response.json();
            this.filteredEmployees = [...this.employees]; // Make a copy for filtering
            this.totalPages = Math.ceil(this.employees.length / this.rowsPerPage);

            // Render the table and pagination
            this.renderTable();
            this.renderPagination();
        } catch (error) {
            console.error('Error fetching employee data:', error);
        }
    }

    renderTable() {
        const start = (this.currentPage - 1) * this.rowsPerPage;
        const end = start + this.rowsPerPage;
        const pageEmployees = this.filteredEmployees.slice(start, end);

        this.tableBody.innerHTML = pageEmployees.map(employee => `
            <tr>
                <td>${employee.employee_id}</td>
                <td>${employee.name}</td>
                <td>${employee.department}</td>
                <td>
                    <button class="view-btn">
                        <i class="fas fa-eye"></i> View
                    </button>
                </td>
            </tr>
        `).join('');

        // Add hover effect to each row
        const rows = this.tableBody.querySelectorAll('tr');
        rows.forEach(row => {
            row.addEventListener('mouseenter', () => {
                row.style.transform = 'translateY(-2px) scale(1.01)';
                row.style.boxShadow = 'var(--shadow-md)';
            });

            row.addEventListener('mouseleave', () => {
                row.style.transform = 'none';
                row.style.boxShadow = 'none';
            });
        });
    }

    renderPagination() {
        this.totalPages = Math.ceil(this.filteredEmployees.length / this.rowsPerPage);

        // No pagination buttons in this version; dynamically calculated based on rowsPerPage

        // If you want pagination, you can add next/previous button logic here
    }

    setupEventListeners() {
        // Search functionality
        this.searchInput.addEventListener('input', (e) => {
            const searchTerm = e.target.value.toLowerCase();
            this.filteredEmployees = this.employees.filter(employee =>
                employee.name.toLowerCase().includes(searchTerm) ||
                employee.department.toLowerCase().includes(searchTerm) ||
                employee.employee_id.toString().includes(searchTerm)
            );
            this.currentPage = 1; // Reset to first page after search
            this.renderTable();
        });
    }
}

// Initialize the employee table when the page loads
document.addEventListener('DOMContentLoaded', () => {
    // Initialize employee table
    new EmployeeTable();

    // Theme toggle functionality
    const body = document.querySelector('body');
    const themeToggle = document.querySelector('.theme-toggle');
    const themeIcon = themeToggle.querySelector('i');
    const themeText = themeToggle.querySelector('span');

    themeToggle.addEventListener('click', () => {
        const isDark = body.getAttribute('data-theme') === 'dark';
        body.setAttribute('data-theme', isDark ? 'light' : 'dark');

        // Update icon and text
        themeIcon.className = isDark ? 'fas fa-moon' : 'fas fa-sun';
        themeText.textContent = isDark ? 'Dark Mode' : 'Light Mode';

        // Add rotation animation
        themeIcon.style.transform = `rotate(${isDark ? '0' : '360'}deg)`;
    });
});
