sed -ie "s/Bearer .*/Bearer token/g" tests/cassettes/github_requests.yaml
sed -ie "s/gh[a-z]_[A-Za-z0-9]*/token/g" tests/cassettes/github_requests.yaml
rm tests/cassettes/github_requests.yamle
