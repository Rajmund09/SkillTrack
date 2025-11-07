
window.addEventListener('load', function () {
    setTimeout(function () {
        document.getElementById('initial-loader').style.opacity = '0';
        setTimeout(function () {
            document.getElementById('initial-loader').style.display = 'none';
        }, 500);
    }, 1500);

    initPageNavigation();

    initDropdowns();
    initSuggestionDropdowns();
});

function initPageNavigation() {
    const startAnalyzeBtn = document.getElementById('start-analyze');
    const backButton = document.getElementById('back-button');
    const landingPage = document.getElementById('landing-page');
    const dashboardPage = document.getElementById('dashboard-page');

    startAnalyzeBtn.addEventListener('click', function (e) {
        e.preventDefault();
        landingPage.style.display = 'none';
        dashboardPage.style.display = 'block';
    });

    backButton.addEventListener('click', function () {
        dashboardPage.style.display = 'none';
        landingPage.style.display = 'flex';
    });
}


function initDropdowns() {
    const dropdownBtn = document.querySelector('.dropdown-btn');
    const dropdownContent = document.querySelector('.dropdown-content');

    dropdownBtn.addEventListener('click', function () {
        dropdownContent.classList.toggle('show');
    });

    window.addEventListener('click', function (e) {
        if (!e.target.closest('.dropdown-btn') && !e.target.closest('.dropdown-content')) {
            if (dropdownContent.classList.contains('show')) {
                dropdownContent.classList.remove('show');
            }
        }
    });
    const options = document.querySelectorAll('.dropdown-option');
    options.forEach(option => {
        option.addEventListener('click', function () {
            const action = option.querySelector('span').textContent;

            if (action === 'Export Data') {
                window.location.href = '/download-csv';
            } else if (action === 'Change Theme') {
                alert('Theme switching coming soon!');
            } else if (action === 'View Analytics') {
                alert('You are already viewing analytics!');
            } else if (action === 'Help & Support') {
                alert('Help & Support coming soon!');
            }

            dropdownContent.classList.remove('show');
        });
    });
}

function initSuggestionDropdowns() {
    const jobRoleInput = document.getElementById('job-role');
    const userSkillsInput = document.getElementById('user-skills');
    const roleSuggestions = document.getElementById('role-suggestions');
    const skillSuggestions = document.getElementById('skill-suggestions');

    jobRoleInput.addEventListener('focus', function () {
        roleSuggestions.style.display = 'block';
    });

    jobRoleInput.addEventListener('blur', function () {
        setTimeout(() => {
            roleSuggestions.style.display = 'none';
        }, 200);
    });

    userSkillsInput.addEventListener('focus', function () {
        skillSuggestions.style.display = 'block';
    });

    userSkillsInput.addEventListener('blur', function () {
        setTimeout(() => {
            skillSuggestions.style.display = 'none';
        }, 200);
    });


    document.querySelectorAll('.suggestion-item').forEach(item => {
        item.addEventListener('mousedown', function () {
            if (this.parentElement.id === 'role-suggestions') {
                jobRoleInput.value = this.textContent;
                roleSuggestions.style.display = 'none';
            } else {

                const currentSkills = userSkillsInput.value;
                if (currentSkills) {
                    userSkillsInput.value = currentSkills + ', ' + this.textContent.toLowerCase();
                } else {
                    userSkillsInput.value = this.textContent.toLowerCase();
                }
                skillSuggestions.style.display = 'none';
            }
        });
    });
}

const searchButton = document.getElementById('search-button');
const jobRoleInput = document.getElementById('job-role');
const userSkillsInput = document.getElementById('user-skills');
const loadingText = document.getElementById('loading');

const skillChartDiv = document.getElementById('skill-chart');
const locChartDiv = document.getElementById('loc-chart');
const expChartDiv = document.getElementById('exp-chart');

const scorePercent = document.getElementById('score-percent');
const scoreText = document.getElementById('score-text');
const missingList = document.getElementById('missing-skills-list');

searchButton.onclick = async function () {
    const jobRole = jobRoleInput.value;
    const userSkills = userSkillsInput.value;
    const location = document.getElementById('location').value;
    const experienceLevel = document.getElementById('experience-level').value;

    if (!jobRole) {
        alert('Please enter a job role.');
        return;
    }

    loadingText.style.display = 'block';
    skillChartDiv.innerHTML = '<h3><i class="fas fa-fire"></i> Top Skills in Demand</h3><p>Loading...</p>';
    locChartDiv.innerHTML = '<h3><i class="fas fa-map-marker-alt"></i> Job Locations</h3><p>Loading...</p>';
    expChartDiv.innerHTML = '<h3><i class="fas fa-briefcase"></i> Experience Level Distribution</h3><p>Loading...</p>';
    scorePercent.innerText = '...';
    scoreText.innerText = 'Analyzing...';
    missingList.innerHTML = '<li>Analyzing...</li>';

    try {
        const response = await fetch('/search', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                'role': jobRole,
                'user_skills': userSkills,
                'location': location,
                'experience_level': experienceLevel,
            })
        });

        if (!response.ok) {
            throw new Error('Server returned an error.');
        }
        const data = await response.json();

        if (data.error) {
            throw new Error(data.error);
        }


        loadingText.style.display = 'none';

        skillChartDiv.innerHTML = data.skill_chart_div;
        if (data.skill_chart_script) {
            const scriptTag = document.createRange().createContextualFragment(data.skill_chart_script);
            document.body.appendChild(scriptTag);
        }

        locChartDiv.innerHTML = data.loc_chart_div;
        if (data.loc_chart_script) {
            const scriptTag = document.createRange().createContextualFragment(data.loc_chart_script);
            document.body.appendChild(scriptTag);
        }

        expChartDiv.innerHTML = data.exp_chart_div;
        if (data.exp_chart_script) {
            const scriptTag = document.createRange().createContextualFragment(data.exp_chart_script);
            document.body.appendChild(scriptTag);
        }

        const suggestions = data.suggestions;
        scorePercent.innerText = suggestions.score + '%';
        scoreText.innerText = `You have ${suggestions.match_count} out of the ${suggestions.total_top_skills} top skills.`;

        missingList.innerHTML = '';
        if (suggestions.missing_skills.length === 0) {
            missingList.innerHTML = '<li>🏆 Great job! You have all the top skills!</li>';
        } else {
            suggestions.missing_skills.forEach(item => {
                const li = document.createElement('li');
                li.innerText = `${item[0].capitalize()} (in ${item[1]} jobs)`;
                missingList.appendChild(li);
            });
        }

    } catch (error) {
        loadingText.style.display = 'none';
        alert('An error occurred: ' + error.message);
    }
};

String.prototype.capitalize = function () {
    return this.charAt(0).toUpperCase() + this.slice(1);
}

// Add filter toggle functionality
const filterToggle = document.getElementById('filter-toggle');
const advancedFilters = document.getElementById('advanced-filters');

filterToggle.addEventListener('click', function () {
    if (advancedFilters.style.display === 'block') {
        advancedFilters.style.display = 'none';
        filterToggle.innerHTML = '<i class="fas fa-filter"></i> Advanced Filters';
    } else {
        advancedFilters.style.display = 'block';
        filterToggle.innerHTML = '<i class="fas fa-times"></i> Hide Filters';
    }
});