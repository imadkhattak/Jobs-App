// DOM Elements
const uploadBox = document.getElementById('uploadBox');
const cvFile = document.getElementById('cvFile');
const browseBtn = document.getElementById('browseBtn');
const filePreview = document.getElementById('filePreview');
const fileName = document.getElementById('fileName');
const fileSize = document.getElementById('fileSize');
const removeBtn = document.getElementById('removeBtn');
const analyzeBtn = document.getElementById('analyzeBtn');
const loading = document.getElementById('loading');
const resultsSection = document.getElementById('resultsSection');
const jobsGrid = document.getElementById('jobsGrid');
const resultsCount = document.getElementById('resultsCount');
const errorMessage = document.getElementById('errorMessage');
const errorText = document.getElementById('errorText');
const retryBtn = document.getElementById('retryBtn');

let selectedFile = null;

// File Upload Handlers
browseBtn.addEventListener('click', () => {
    cvFile.click();
});

uploadBox.addEventListener('click', () => {
    cvFile.click();
});

cvFile.addEventListener('change', (e) => {
    handleFileSelect(e.target.files[0]);
});

// Drag and Drop
uploadBox.addEventListener('dragover', (e) => {
    e.preventDefault();
    uploadBox.classList.add('drag-over');
});

uploadBox.addEventListener('dragleave', () => {
    uploadBox.classList.remove('drag-over');
});

uploadBox.addEventListener('drop', (e) => {
    e.preventDefault();
    uploadBox.classList.remove('drag-over');
    
    const file = e.dataTransfer.files[0];
    handleFileSelect(file);
});

// Handle File Selection
function handleFileSelect(file) {
    if (!file) return;

    // Validate file type
    const validTypes = ['application/pdf', 'application/msword', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'];
    if (!validTypes.includes(file.type)) {
        showError('Invalid file type. Please upload a PDF, DOC, or DOCX file.');
        return;
    }

    // Validate file size (16MB)
    if (file.size > 16 * 1024 * 1024) {
        showError('File size exceeds 16MB. Please upload a smaller file.');
        return;
    }

    selectedFile = file;
    
    // Show file preview
    fileName.textContent = file.name;
    fileSize.textContent = formatFileSize(file.size);
    
    uploadBox.style.display = 'none';
    filePreview.style.display = 'block';
    
    // Hide previous results/errors
    resultsSection.style.display = 'none';
    errorMessage.style.display = 'none';
}

// Remove File
removeBtn.addEventListener('click', () => {
    selectedFile = null;
    cvFile.value = '';
    uploadBox.style.display = 'block';
    filePreview.style.display = 'none';
});

// Analyze CV
analyzeBtn.addEventListener('click', async () => {
    if (!selectedFile) return;

    // Show loading state
    filePreview.style.display = 'none';
    loading.style.display = 'block';
    resultsSection.style.display = 'none';
    errorMessage.style.display = 'none';

    const formData = new FormData();
    formData.append('cv_file', selectedFile);

    try {
        const response = await fetch('/upload', {
            method: 'POST',
            body: formData
        });

        const data = await response.json();

        if (response.ok && data.success) {
            displayResults(data.jobs);
        } else {
            showError(data.error || 'An error occurred while processing your CV.');
        }
    } catch (error) {
        showError('Network error. Please check your connection and try again.');
    } finally {
        loading.style.display = 'none';
    }
});

let jobs = [];

// Display Results
function displayResults(jobData) {
    jobs = jobData;
    jobsGrid.innerHTML = '';
    
    if (!jobs || jobs.length === 0) {
        showError('No matching jobs found. Please try with a different CV.');
        return;
    }

    resultsCount.textContent = `Found ${jobs.length} matching opportunities`;
    resultsSection.style.display = 'block';

    jobs.forEach(job => {
        const card = createJobCard(job);
        jobsGrid.appendChild(card);
    });

    // Scroll to results
    resultsSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

// Create Job Card
function createJobCard(job) {
    const card = document.createElement('div');
    card.className = 'job-card';

    const score = job['Relevance Score'] || 0;
    const scoreClass = score >= 70 ? 'score-high' : score >= 40 ? 'score-medium' : 'score-low';

    const missingSkills = job['Missing Skills'] || [];
    const skillsHTML = missingSkills.length > 0
        ? missingSkills.map(skill => `<span class="skill-tag">${skill}</span>`).join('')
        : '<span class="no-missing-skills"><i class="fas fa-check-circle"></i> All skills matched!</span>';

    let salaryHTML = '';
    if (job['Salary']) {
        salaryHTML = `<div class="salary"><i class="fas fa-dollar-sign"></i> ${job['Salary']}</div>`;
    }

    card.innerHTML = `
        <div class="job-header">
            <div>
                <h3 class="job-title">${job['Job Title'] || 'N/A'}</h3>
                <div class="company-name">
                    <i class="fas fa-building"></i>
                    ${job['Company'] || 'N/A'}
                </div>
            </div>
            <div class="score-badge ${scoreClass}">
                ${score}%
            </div>
        </div>
        ${salaryHTML}
        <div class="skills-section">
            <span class="skills-label">
                ${missingSkills.length > 0 ? 'Missing Skills:' : 'Match Status:'}
            </span>
            <div class="skills-list">
                ${skillsHTML}
            </div>
        </div>
        <div class="job-card-buttons">
            <a href="${job['Job Link'] || '#'}" target="_blank" class="apply-btn">Apply Now</a>
            <button class="save-job-btn" data-job-title="${job['Job Title']}" data-job-company="${job['Company']}">Save Job</button>
        </div>
    `;

    // Add click animation
    card.addEventListener('click', (e) => {
        if (e.target.tagName !== 'A' && e.target.tagName !== 'BUTTON') {
            card.style.transform = 'scale(0.98)';
            setTimeout(() => {
                card.style.transform = '';
            }, 200);
        }
    });

    return card;
}

// Save Job
async function saveJob(job) {
    try {
        const response = await fetch('/save_job', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(job)
        });

        const data = await response.json();

        if (data.success) {
            alert('Job saved successfully!');
        } else {
            alert('Failed to save job: ' + data.error);
        }
    } catch (error) {
        alert('Network error. Please check your connection and try again.');
    }
}

document.addEventListener('click', (e) => {
    if (e.target.classList.contains('save-job-btn')) {
        const jobTitle = e.target.dataset.jobTitle;
        const jobCompany = e.target.dataset.jobCompany;
        const job = jobs.find(j => j['Job Title'] === jobTitle && j['Company'] === jobCompany);
        if (job) {
            saveJob(job);
        }
    }
});

// Show Error
function showError(message) {
    errorText.textContent = message;
    errorMessage.style.display = 'block';
    filePreview.style.display = 'none';
    uploadBox.style.display = 'none';
}

// Retry Button
retryBtn.addEventListener('click', () => {
    selectedFile = null;
    cvFile.value = '';
    uploadBox.style.display = 'block';
    filePreview.style.display = 'none';
    errorMessage.style.display = 'none';
    resultsSection.style.display = 'none';
});

// Format File Size
function formatFileSize(bytes) {
    if (bytes < 1024) return bytes + ' B';
    if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(2) + ' KB';
    return (bytes / (1024 * 1024)).toFixed(2) + ' MB';
}

// Smooth Animations on Load
document.addEventListener('DOMContentLoaded', () => {
    const header = document.querySelector('.header');
    const uploadSection = document.querySelector('.upload-section');
    
    header.style.opacity = '0';
    header.style.transform = 'translateY(-20px)';
    uploadSection.style.opacity = '0';
    uploadSection.style.transform = 'translateY(20px)';
    
    setTimeout(() => {
        header.style.transition = 'all 0.6s ease';
        header.style.opacity = '1';
        header.style.transform = 'translateY(0)';
    }, 100);
    
    setTimeout(() => {
        uploadSection.style.transition = 'all 0.6s ease';
        uploadSection.style.opacity = '1';
        uploadSection.style.transform = 'translateY(0)';
    }, 300);
});