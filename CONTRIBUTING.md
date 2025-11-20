# Contributing to DoseSafe AI 🤝

We love your input! We want to make contributing to DoseSafe AI as easy and transparent as possible, whether it's:

- Reporting a bug
- Discussing the current state of the code
- Submitting a fix
- Proposing new features
- Becoming a maintainer

## 🚀 Development Process

We use GitHub to host code, to track issues and feature requests, as well as accept pull requests.

### 1. Fork the Repository
```bash
# Fork the repo on GitHub, then clone your fork
git clone https://github.com/yourusername/dosesafe-ai.git
cd dosesafe-ai

# Add the original repository as upstream
git remote add upstream https://github.com/originalowner/dosesafe-ai.git
```

### 2. Set Up Development Environment
```bash
# Backend setup
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # macOS/Linux
pip install -r requirements.txt

# Frontend setup
cd ../frontend
npm install
```

### 3. Create a Feature Branch
```bash
# Create and switch to a new branch
git checkout -b feature/amazing-new-feature

# Or for bug fixes
git checkout -b fix/bug-description
```

### 4. Make Your Changes
- Write clean, readable code
- Follow existing code style and conventions
- Add tests for new functionality
- Update documentation as needed

### 5. Test Your Changes
```bash
# Run backend tests
cd backend
python -m pytest

# Run frontend tests
cd frontend
npm test

# Test the full application
npm run build
```

### 6. Commit Your Changes
```bash
# Stage your changes
git add .

# Commit with a descriptive message
git commit -m "feat: add AI-powered drug name correction

- Implement fuzzy matching for medication names
- Add confidence scoring for OCR results
- Update API documentation"
```

### 7. Push and Create Pull Request
```bash
# Push to your fork
git push origin feature/amazing-new-feature

# Create a pull request on GitHub
```

## 📝 Commit Message Convention

We follow [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

### Types:
- `feat`: A new feature
- `fix`: A bug fix
- `docs`: Documentation only changes
- `style`: Changes that do not affect the meaning of the code
- `refactor`: A code change that neither fixes a bug nor adds a feature
- `perf`: A code change that improves performance
- `test`: Adding missing tests or correcting existing tests
- `chore`: Changes to the build process or auxiliary tools

### Examples:
```bash
feat(ocr): add support for PDF prescription scanning
fix(api): resolve medication name parsing edge case
docs: update API documentation for new endpoints
style(frontend): improve button hover animations
refactor(backend): optimize database queries
test(ocr): add unit tests for image preprocessing
chore: update dependencies to latest versions
```

## 🐛 Bug Reports

Great bug reports tend to have:

- A quick summary and/or background
- Steps to reproduce
  - Be specific!
  - Give sample code if you can
- What you expected would happen
- What actually happens
- Notes (possibly including why you think this might be happening, or stuff you tried that didn't work)

### Bug Report Template:
```markdown
**Bug Description**
A clear and concise description of what the bug is.

**To Reproduce**
Steps to reproduce the behavior:
1. Go to '...'
2. Click on '....'
3. Scroll down to '....'
4. See error

**Expected Behavior**
A clear and concise description of what you expected to happen.

**Screenshots**
If applicable, add screenshots to help explain your problem.

**Environment:**
 - OS: [e.g. Windows 10]
 - Browser [e.g. chrome, safari]
 - Version [e.g. 22]
 - Python version: [e.g. 3.9]
 - Node version: [e.g. 18.0.0]

**Additional Context**
Add any other context about the problem here.
```

## ✨ Feature Requests

We track feature requests as [GitHub issues](https://github.com/yourusername/dosesafe-ai/issues).

### Feature Request Template:
```markdown
**Is your feature request related to a problem? Please describe.**
A clear and concise description of what the problem is.

**Describe the solution you'd like**
A clear and concise description of what you want to happen.

**Describe alternatives you've considered**
A clear and concise description of any alternative solutions or features you've considered.

**Additional context**
Add any other context or screenshots about the feature request here.
```

## 🎯 Areas We Need Help With

### 🔥 High Priority
- [ ] Improve OCR accuracy for handwritten prescriptions
- [ ] Add support for more international drug databases
- [ ] Implement real-time collaboration features
- [ ] Enhance mobile responsiveness
- [ ] Add comprehensive test coverage

### 🚀 New Features
- [ ] Multi-language support
- [ ] Voice input for medication entry
- [ ] Integration with pharmacy systems
- [ ] Allergy checking and warnings
- [ ] Medication reminder system

### 🐛 Bug Fixes
- [ ] Fix image upload issues on mobile Safari
- [ ] Resolve medication name parsing edge cases
- [ ] Improve error handling for API timeouts

### 📚 Documentation
- [ ] API documentation improvements
- [ ] Video tutorials for setup
- [ ] Deployment guides for various platforms
- [ ] User manual with examples

## 🧪 Testing Guidelines

### Backend Testing
```bash
# Run all tests
python -m pytest

# Run tests with coverage
python -m pytest --cov=.

# Run specific test file
python -m pytest tests/test_ocr.py
```

### Frontend Testing
```bash
# Run unit tests
npm test

# Run tests in watch mode
npm test -- --watch

# Run tests with coverage
npm test -- --coverage
```

### Integration Testing
- Test the complete prescription scanning pipeline
- Verify API endpoints work correctly
- Ensure frontend-backend communication

## 📋 Code Style Guidelines

### Python (Backend)
- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/)
- Use [Black](https://black.readthedocs.io/) for code formatting
- Use type hints where possible
- Write docstrings for all functions and classes

```python
def extract_medications(text: str, confidence_threshold: float = 0.8) -> List[Dict[str, Any]]:
    """
    Extract medication information from OCR text.
    
    Args:
        text: Raw OCR text from prescription image
        confidence_threshold: Minimum confidence score for extraction
        
    Returns:
        List of dictionaries containing medication information
    """
    pass
```

### JavaScript/React (Frontend)
- Use [Prettier](https://prettier.io/) for code formatting
- Follow [Airbnb JavaScript Style Guide](https://github.com/airbnb/javascript)
- Use functional components with hooks
- Write JSDoc comments for complex functions

```javascript
/**
 * Process image scan and extract medication data
 * @param {File} file - Prescription image file
 * @param {number} patientAge - Patient age for age-specific warnings
 * @param {string} patientCondition - Patient medical condition
 * @returns {Promise<ScanResult>} Processed scan results
 */
const processImageScan = async (file, patientAge, patientCondition) => {
  // Implementation
};
```

## 🔐 Security Guidelines

- Never commit API keys or sensitive data
- Use environment variables for configuration
- Validate all user inputs
- Implement proper error handling
- Follow OWASP security guidelines

## 📱 Platform-Specific Guidelines

### Mobile Development
- Test on both iOS and Android devices
- Ensure touch interactions work properly
- Optimize for different screen sizes
- Consider offline functionality

### Web Accessibility
- Follow WCAG 2.1 guidelines
- Ensure keyboard navigation works
- Add proper ARIA labels
- Test with screen readers

## 🎉 Recognition

Contributors will be recognized in:
- README contributors section
- Release notes
- Project documentation
- Special contributor badges

## 📞 Questions?

- 💬 **Discussions**: [GitHub Discussions](https://github.com/yourusername/dosesafe-ai/discussions)
- 📧 **Email**: contributors@dosesafe-ai.com
- 🐛 **Issues**: [GitHub Issues](https://github.com/yourusername/dosesafe-ai/issues)

## 📄 License

By contributing, you agree that your contributions will be licensed under the same [MIT License](LICENSE) that covers the project.

---

**Thank you for contributing to DoseSafe AI! 🙏**

Together, we're making medication safety accessible to everyone.
