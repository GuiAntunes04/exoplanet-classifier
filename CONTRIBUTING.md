# 🤝 Contributing Guide

Thank you for considering contributing to the Exoplanet Classifier! This document provides guidelines for contributions.

## 📋 How to Contribute

### 1. Fork and Clone
```bash
# Fork the repository on GitHub
# Clone your fork
git clone https://github.com/your-username/exoplanet-classifier.git
cd exoplanet-classifier
```

### 2. Setup Environment
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt
```

### 3. Create Branch
```bash
git checkout -b feature/new-feature
# or
git checkout -b fix/bug-fix
```

## 🎯 Types of Contributions

### 🐛 Report Bugs
1. Check if the bug has already been reported
2. Use the issue template
3. Include:
   - Clear description of the problem
   - Steps to reproduce
   - Expected vs actual behavior
   - Screenshots if applicable

### ✨ Suggest Features
1. Check if the feature has already been suggested
2. Describe the feature in detail
3. Explain the value to users
4. Consider implementation complexity

### 💻 Contribute Code

#### Code Standards
- Use Python 3.9+
- Follow PEP 8
- Use type hints when possible
- Document functions and classes

#### Commit Structure
```
type(scope): description

Body of the message explaining what and why.

Fixes #123
```

Types:
- `feat`: new feature
- `fix`: bug fix
- `docs`: documentation
- `style`: formatting
- `refactor`: refactoring
- `test`: tests
- `chore`: maintenance tasks

#### Example
```bash
git commit -m "feat(ui): add loading animation

Implements loading spinner during data processing
to improve UX.

Fixes #45"
```

## 🧪 Testing

### Run Tests
```bash
# Install test dependencies
pip install pytest pytest-cov

# Run tests
pytest

# With coverage
pytest --cov=app
```

### Write Tests
```python
def test_classification_function():
    """Test classification function."""
    # Arrange
    input_data = {...}
    expected = "EXOPLANET"
    
    # Act
    result = classify_exoplanet(input_data)
    
    # Assert
    assert result == expected
```

## 📝 Documentation

### Update README
- Keep instructions updated
- Add screenshots when necessary
- Document new features

### Code Comments
```python
def prepare_data_for_model(data_dict, train_features):
    """
    Prepare data for classification model.
    
    Args:
        data_dict (dict): User input data
        train_features (list): Model features list
        
    Returns:
        pd.DataFrame: Processed data for prediction
    """
    # Implementation...
```

## 🎨 Interface

### UI Standards
- Maintain visual consistency
- Use existing space theme
- Test on different resolutions
- Consider accessibility

### CSS/Style
```css
/* Use CSS variables for colors */
:root {
    --primary-color: #4ecdc4;
    --background-color: #0a0a0a;
}

/* Maintain responsiveness */
@media (max-width: 768px) {
    /* Mobile styles */
}
```

## 🔍 Code Review

### Before Submitting
- [ ] Code follows established standards
- [ ] Tests pass
- [ ] Documentation updated
- [ ] Interface tested
- [ ] Performance verified

### Review Process
1. Create Pull Request
2. Fill template
3. Wait for review
4. Make adjustments if necessary
5. Merge after approval

## 📊 Quality Metrics

### Test Coverage
- Minimum: 80%
- Ideal: 90%+

### Performance
- Loading time < 3s
- Optimized memory usage
- Maintained responsiveness

## 🚀 Deploy

### Local Testing
```bash
# Run application
streamlit run app.py

# Check functionality
# Test on different browsers
```

### Test Deploy
- Use development branch
- Test in production-like environment
- Check logs and metrics

## 📞 Communication

### Channels
- **Issues**: For bugs and features
- **Discussions**: For questions and ideas
- **Pull Requests**: For code

### Etiquette
- Be respectful and constructive
- Use clear and objective language
- Help other contributors
- Celebrate contributions

## 🏆 Recognition

### Contributors
- Listed in README
- Mentioned in releases
- Contribution badges

### Types of Contribution
- 🐛 Bug reports
- ✨ Feature requests
- 💻 Code contributions
- 📝 Documentation
- 🎨 Design/UI
- 🧪 Testing
- 📢 Community support

## 📋 Contribution Checklist

### For Issues
- [ ] Clear description
- [ ] Steps to reproduce
- [ ] Expected behavior
- [ ] Screenshots if applicable
- [ ] Appropriate labels

### For Pull Requests
- [ ] Updated branch
- [ ] Descriptive commits
- [ ] Passing tests
- [ ] Updated documentation
- [ ] Tested interface
- [ ] Verified performance

## 🎯 Roadmap

### Upcoming Features
- [ ] REST API
- [ ] More ML algorithms
- [ ] Advanced visualizations
- [ ] Report export
- [ ] Database integration

### Technical Improvements
- [ ] Automated tests
- [ ] CI/CD pipeline
- [ ] Monitoring
- [ ] Data caching
- [ ] Performance optimizations

---

**Thank you for contributing! 🌟**

Every contribution, no matter how small, makes a difference for the astronomical community.
