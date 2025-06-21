#!/bin/bash

# URL validation script
# Checks HTTP status codes and looks for canonical URLs

echo "URL Validation Report"
echo "===================="
echo "Checking all URLs in urls-list.md..."
echo ""

# Create CSV header
echo "id,url,status,canonical" > url-validation-report.csv

# Extract and validate URLs
while IFS= read -r line; do
    # Extract id and url from the format {id: X, url: "Y"}
    if [[ $line =~ \{id:[[:space:]]*([0-9]+),[[:space:]]*url:[[:space:]]*\"([^\"]+)\"\} ]]; then
        id="${BASH_REMATCH[1]}"
        url="${BASH_REMATCH[2]}"
        
        echo -n "Checking ID $id: $url ... "
        
        # Get HTTP status code
        status=$(curl -s -o /dev/null -w "%{http_code}" -L --max-time 10 "$url")
        
        # Get canonical URL from headers if exists
        canonical=$(curl -sI -L --max-time 10 "$url" | grep -i '^link:.*rel="canonical"' | sed -E 's/.*<([^>]+)>.*/\1/' | tr -d '\r')
        
        # If no canonical in headers, check for it in HTML meta tags
        if [ -z "$canonical" ]; then
            canonical=$(curl -s -L --max-time 10 "$url" | grep -E '<link[^>]+rel="canonical"[^>]*>' | sed -E 's/.*href="([^"]+)".*/\1/' | head -1)
        fi
        
        # Print status
        if [ "$status" = "200" ]; then
            echo "✓ OK ($status)"
        else
            echo "✗ FAIL ($status)"
        fi
        
        # Write to CSV
        echo "$id,\"$url\",$status,\"$canonical\"" >> url-validation-report.csv
        
        # Check for problematic patterns
        if [[ $url =~ /tree/[0-9a-f]{7,40} ]]; then
            echo "  ⚠️  WARNING: URL contains commit hash"
        fi
        if [[ $url =~ /releases/tag/v[0-9]+\.[0-9]+ ]]; then
            echo "  ⚠️  WARNING: URL points to specific version tag"
        fi
        
        # Rate limiting
        sleep 0.5
    fi
done < urls-list.md

echo ""
echo "Validation complete! Results saved to url-validation-report.csv"
echo ""

# Summary statistics
total=$(grep -c '^[0-9]' url-validation-report.csv)
ok_count=$(grep -c ',200,' url-validation-report.csv)
fail_count=$((total - ok_count))

echo "Summary:"
echo "  Total URLs checked: $total"
echo "  Successful (200 OK): $ok_count"
echo "  Failed/Redirected: $fail_count"