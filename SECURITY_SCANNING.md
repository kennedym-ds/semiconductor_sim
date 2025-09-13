# Security Scanning Configuration

This document describes the security scanning setup for the semiconductor_sim project.

## Bandit Static Security Analysis

### Configuration
- Configuration file: `bandit.yaml`
- Scans: `semiconductor_sim/` package (excludes tests, build artifacts)
- Threshold: Medium severity and confidence for CI failures
- Output: JSON artifacts uploaded to CI for each build

### Current Baseline
As of the security implementation (2025-09):
- **Total lines scanned**: 946
- **Issues found**: 2 low-severity findings (B110: try-except-pass patterns)
- **Critical issues**: 0 medium+ severity issues
- **Status**: ✅ Clean baseline for critical security checks

### CI Integration
1. **Non-blocking scan**: Generates full JSON report as artifact
2. **Blocking check**: Fails CI only on medium+ severity issues
3. **Future enhancement**: Can be made fully blocking once baseline is established

## CodeQL Analysis

### Configuration
- **Query suite**: `security-and-quality` (enhanced from default)
- **Language**: Python
- **Schedule**: Push, PR, and weekly scans
- **Coverage**: Full source code analysis including security patterns

### Features
- Advanced security pattern detection
- Quality checks for maintainability
- Automated vulnerability discovery
- SARIF integration with GitHub Security tab

## Usage

### Local Security Scanning
```bash
# Run bandit locally
bandit -c bandit.yaml -r semiconductor_sim/

# Run with CI thresholds
bandit -c bandit.yaml -r semiconductor_sim/ --severity-level medium --confidence-level medium

# Generate JSON report
bandit -c bandit.yaml -r semiconductor_sim/ -f json -o security-report.json
```

### Customization
To modify security scanning behavior:
1. Edit `bandit.yaml` for scan configuration
2. Update `.github/workflows/ci.yml` for CI integration
3. Adjust severity thresholds as needed

## Security Findings Triage

### Low-Severity Findings (Informational)
- B110: try-except-pass patterns in plotting utilities
- These are acceptable for optional backend configuration
- Consider adding specific exception handling if needed

### Future Considerations
- Monitor for new security findings in dependencies
- Regular security baseline reviews
- Consider adding security tests for input validation