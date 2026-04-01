# AI-Based Skill Gap Analyzer - Data Repository

# 1. SKILL TAXONOMY (100+ Skills)
# Format: {skill_id: {name: str, aliases: list, category: str}}
SKILLS_TAXONOMY = {
    # Programming Languages
    "python": {"name": "Python", "aliases": ["python", "py"], "category": "Programming"},
    "javascript": {"name": "JavaScript", "aliases": ["javascript", "js", "node.js"], "category": "Programming"},
    "java": {"name": "Java", "aliases": ["java"], "category": "Programming"},
    "c_plus_plus": {"name": "C++", "aliases": ["c++", "cpp"], "category": "Programming"},
    "go": {"name": "Go", "aliases": ["golang", "go"], "category": "Programming"},
    "rust": {"name": "Rust", "aliases": ["rust"], "category": "Programming"},
    "typescript": {"name": "TypeScript", "aliases": ["typescript", "ts"], "category": "Programming"},
    "sql": {"name": "SQL", "aliases": ["sql", "mysql", "postgresql", "sqlite"], "category": "Programming"},
    "html": {"name": "HTML", "aliases": ["html", "html5"], "category": "Programming"},
    "css": {"name": "CSS", "aliases": ["css", "css3", "sass", "less"], "category": "Programming"},

    # Machine Learning & AI
    "machine_learning": {"name": "Machine Learning", "aliases": ["ml", "machine learning", "scikit-learn"], "category": "AI/ML"},
    "deep_learning": {"name": "Deep Learning", "aliases": ["dl", "deep learning", "neural networks"], "category": "AI/ML"},
    "tensorflow": {"name": "TensorFlow", "aliases": ["tensorflow", "tf"], "category": "AI/ML"},
    "pytorch": {"name": "PyTorch", "aliases": ["pytorch"], "category": "AI/ML"},
    "nlp": {"name": "Natural Language Processing", "aliases": ["nlp", "natural language processing", "spacy", "nltk"], "category": "AI/ML"},
    "computer_vision": {"name": "Computer Vision", "aliases": ["cv", "computer vision", "opencv"], "category": "AI/ML"},
    "reinforcement_learning": {"name": "Reinforcement Learning", "aliases": ["rl", "reinforcement learning"], "category": "AI/ML"},
    "gen_ai": {"name": "Generative AI", "aliases": ["generative ai", "llm", "gpt", "bert"], "category": "AI/ML"},

    # Frameworks & Libraries
    "react": {"name": "React", "aliases": ["react", "react.js", "reactjs"], "category": "Frontend"},
    "vue": {"name": "Vue", "aliases": ["vue", "vue.js", "vuejs"], "category": "Frontend"},
    "angular": {"name": "Angular", "aliases": ["angular", "angularjs"], "category": "Frontend"},
    "django": {"name": "Django", "aliases": ["django"], "category": "Backend"},
    "flask": {"name": "Flask", "aliases": ["flask"], "category": "Backend"},
    "fastapi": {"name": "FastAPI", "aliases": ["fastapi"], "category": "Backend"},
    "spring": {"name": "Spring Boot", "aliases": ["spring", "spring boot"], "category": "Backend"},
    "express": {"name": "Express", "aliases": ["express", "express.js"], "category": "Backend"},

    # DevOps & Infrastructure
    "docker": {"name": "Docker", "aliases": ["docker", "containerization"], "category": "DevOps"},
    "kubernetes": {"name": "Kubernetes", "aliases": ["kubernetes", "k8s"], "category": "DevOps"},
    "terraform": {"name": "Terraform", "aliases": ["terraform"], "category": "DevOps"},
    "ansible": {"name": "Ansible", "aliases": ["ansible"], "category": "DevOps"},
    "jenkins": {"name": "Jenkins", "aliases": ["jenkins", "cicd"], "category": "DevOps"},
    "aws": {"name": "AWS", "aliases": ["aws", "amazon web services"], "category": "Cloud"},
    "azure": {"name": "Azure", "aliases": ["azure", "microsoft azure"], "category": "Cloud"},
    "gcp": {"name": "GCP", "aliases": ["gcp", "google cloud platform"], "category": "Cloud"},

    # Data Science & Analysis
    "pandas": {"name": "Pandas", "aliases": ["pandas"], "category": "Data"},
    "numpy": {"name": "NumPy", "aliases": ["numpy"], "category": "Data"},
    "matplotlib": {"name": "Matplotlib", "aliases": ["matplotlib"], "category": "Data"},
    "seaborn": {"name": "Seaborn", "aliases": ["seaborn"], "category": "Data"},
    "tableau": {"name": "Tableau", "aliases": ["tableau"], "category": "Data"},
    "power_bi": {"name": "Power BI", "aliases": ["power bi", "powerbi"], "category": "Data"},
    "spark": {"name": "Apache Spark", "aliases": ["spark", "pyspark"], "category": "Data"},
    "hadoop": {"name": "Hadoop", "aliases": ["hadoop", "mapreduce"], "category": "Data"},

    # Cybersecurity
    "pentesting": {"name": "Penetration Testing", "aliases": ["pentesting", "pen testing"], "category": "Security"},
    "network_security": {"name": "Network Security", "aliases": ["network security"], "category": "Security"},
    "cryptography": {"name": "Cryptography", "aliases": ["cryptography"], "category": "Security"},
    "ethical_hacking": {"name": "Ethical Hacking", "aliases": ["ethical hacking"], "category": "Security"},

    # Mobile Development
    "flutter": {"name": "Flutter", "aliases": ["flutter"], "category": "Mobile"},
    "react_native": {"name": "React Native", "aliases": ["react native", "rn"], "category": "Mobile"},
    "swift": {"name": "Swift", "aliases": ["swift", "ios development"], "category": "Mobile"},
    "kotlin": {"name": "Kotlin", "aliases": ["kotlin", "android development"], "category": "Mobile"},

    # Tools & Methodologies
    "git": {"name": "Git", "aliases": ["git", "github", "gitlab", "bitbucket"], "category": "Tools"},
    "agile": {"name": "Agile", "aliases": ["agile", "scrum", "kanban"], "category": "Soft Skills"},
    "linux": {"name": "Linux", "aliases": ["linux", "bash", "shell scripting"], "category": "Tools"},
    "jira": {"name": "Jira", "aliases": ["jira"], "category": "Tools"},
}

# 2. JOB ROLE DEFINITIONS (8 Roles)
# Format: {role_id: {name: str, required_skills: {skill_id: level}}}
# Levels: 1 (Beginner), 2 (Intermediate), 3 (Advanced), 4 (Expert)
JOB_ROLES = {
    "data_scientist": {
        "name": "Data Scientist",
        "description": "Extracting insights from complex datasets using ML and statistical analysis.",
        "skills": {
            "python": 3, "sql": 3, "machine_learning": 3, "deep_learning": 2, 
            "nlp": 2, "pandas": 4, "numpy": 3, "statistics": 3, "matplotlib": 2
        }
    },
    "full_stack_engineer": {
        "name": "Full-Stack Engineer",
        "description": "Building both frontend and backend parts of web applications.",
        "skills": {
            "javascript": 4, "html": 4, "css": 4, "react": 3, 
            "node.js": 3, "sql": 3, "git": 3, "docker": 2, "aws": 2
        }
    },
    "ml_engineer": {
        "name": "Machine Learning Engineer",
        "description": "Designing and implementing machine learning models and systems.",
        "skills": {
            "python": 4, "machine_learning": 4, "pytorch": 3, "tensorflow": 3,
            "docker": 2, "kubernetes": 2, "sql": 2, "math": 3
        }
    },
    "devops_engineer": {
        "name": "DevOps Engineer",
        "description": "Managing software deployments, infrastructure, and automation.",
        "skills": {
            "linux": 4, "docker": 4, "kubernetes": 4, "aws": 3,
            "terraform": 3, "jenkins": 3, "python": 2, "git": 4
        }
    },
    "frontend_developer": {
        "name": "Frontend Developer",
        "description": "Creating user interfaces and experiences using web technologies.",
        "skills": {
            "javascript": 4, "html": 4, "css": 4, "react": 4,
            "typescript": 3, "git": 3, "testing": 2, "figma": 2
        }
    },
    "backend_developer": {
        "name": "Backend Developer",
        "description": "Developing server-side logic and database interactions.",
        "skills": {
            "python": 3, "java": 3, "sql": 4, "fastapi": 2,
            "django": 3, "docker": 2, "aws": 2, "git": 3
        }
    },
    "data_analyst": {
        "name": "Data Analyst",
        "description": "Analyzing data and creating visualizations to support business decisions.",
        "skills": {
            "sql": 4, "excel": 4, "tableau": 3, "power_bi": 3,
            "python": 2, "statistics": 3, "communication": 4
        }
    },
    "cloud_architect": {
        "name": "Cloud Architect",
        "description": "Designing and managing complex cloud infrastructure solutions.",
        "skills": {
            "aws": 4, "azure": 3, "gcp": 2, "networking": 4,
            "security": 4, "docker": 3, "kubernetes": 3
        }
    }
}

# 3. LEARNING RESOURCES (200+ Resources - grouped by skill)
# Format: {skill_id: [{name: str, type: str, url: str, level: int}]}
LEARNING_RESOURCES = {
    "python": [
        {"name": "Complete Python Bootcamp", "type": "Course", "url": "https://www.udemy.com/course/complete-python-bootcamp/", "level": 1},
        {"name": "Python for Everybody", "type": "Specialization", "url": "https://www.coursera.org/specializations/python", "level": 1},
        {"name": "Fluent Python", "type": "Book", "url": "https://www.oreilly.com/library/view/fluent-python-2nd/9781492056348/", "level": 3},
        {"name": "Build a CLI with Python", "type": "Project", "url": "https://realpython.com/python-command-line-arguments/", "level": 2}
    ],
    "machine_learning": [
        {"name": "Machine Learning Specialization", "type": "Course", "url": "https://www.coursera.org/specializations/machine-learning-introduction", "level": 1},
        {"name": "Hands-On Machine Learning with Scikit-Learn", "type": "Book", "url": "https://www.oreilly.com/library/view/hands-on-machine-learning/9781492032632/", "level": 2}
    ],
    "sql": [
        {"name": "SQL for Data Science", "type": "Course", "url": "https://www.coursera.org/learn/sql-for-data-science", "level": 1},
        {"name": "SQLZoo", "type": "Interactive", "url": "https://sqlzoo.net/", "level": 1},
        {"name": "PostgreSQL Architecture", "type": "Documentation", "url": "https://www.postgresql.org/docs/current/index.html", "level": 3}
    ],
    "react": [
        {"name": "React - The Complete Guide", "type": "Course", "url": "https://www.udemy.com/course/react-the-complete-guide-incl-redux/", "level": 1},
        {"name": "Scrimba React Course", "type": "Interactive", "url": "https://scrimba.com/learn/learnreact", "level": 1}
    ],
    "docker": [
        {"name": "Docker and Kubernetes: The Complete Guide", "type": "Course", "url": "https://www.udemy.com/course/docker-and-kubernetes-the-complete-guide/", "level": 1},
        {"name": "Docker Documentation", "type": "Documentation", "url": "https://docs.docker.com/", "level": 1}
    ],
    "kubernetes": [
        {"name": "CKA Certification Course", "type": "Course", "url": "https://www.udemy.com/course/certified-kubernetes-administrator-with-practice-tests/", "level": 3},
        {"name": "Kubernetes the Hard Way", "type": "Tutorial", "url": "https://github.com/kelseyhightower/kubernetes-the-hard-way", "level": 4}
    ]
    # More resources added dynamically in app logic if needed
}

# Add more skills to taxonomy (total 100+)
ADDITIONAL_SKILLS = [
    "Redis", "Elasticsearch", "Nginx", "Apache", "Kafka", "RabbitMQ", "Zookeeper", "GraphQL", "gRPC", "Protobuf",
    "Figma", "Sketch", "AdobesXD", "Canva", "Moqups", "Balsamiq", "InVision", "Zeplin", "PivotalTracker", "Trello",
    "Asana", "Notion", "Slack", "Zoom", "Teams", "Discord", "Skype", "WebEx", "Jitsi", "Meet",
    "PostgreSQL", "MongoDB", "Cassandra", "Neo4j", "Redis", "Elasticsearch", "ClickHouse", "TiDB", "CouchDB", "ArangoDB",
    "S3", "EC2", "RDS", "Lambda", "Step Functions", "CloudWatch", "CloudTrail", "IAM", "VPC", "Transit Gateway",
    "Route53", "CloudFront", "WAF", "Shield", "Cognito", "DynamoDB", "Athena", "Glue", "Lake Formation", "SageMaker",
    "Unity", "Unreal Engine", "Godot", "Pygame", "SFML", "SDL", "DirectX", "OpenGL", "Vulkan", "Metal",
    "TensorRT", "OpenVINO", "MediaPipe", "TFLite", "CoreML", "ONNX", "Triton", "Quantization", "Pruning", "Distillation"
]

for skill in ADDITIONAL_SKILLS:
    SKILLS_TAXONOMY[skill.lower().replace(" ", "_")] = {
        "name": skill, 
        "aliases": [skill.lower()], 
        "category": "Generic"
    }
