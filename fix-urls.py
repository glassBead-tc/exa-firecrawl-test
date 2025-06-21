#!/usr/bin/env python3

import json
import re

# Mapping of old URLs to their canonical replacements
URL_REPLACEMENTS = {
    # TanStack replacements
    r"https://github.com/TanStack/table/releases/tag/v7\.0\.0": "https://tanstack.com/table/latest/docs/guide/column-defs",
    r"https://github.com/TanStack/table/tree/v7\.0\.0": "https://tanstack.com/table/latest",
    r"https://github.com/TanStack/table/tree/v6": "https://tanstack.com/table/latest",
    r"https://github.com/TanStack/query/tree/[a-f0-9]+": "https://tanstack.com/query/latest",
    r"https://github.com/tanstack/query": "https://tanstack.com/query/latest",
    r"https://github.com/TanStack/form": "https://tanstack.com/form/latest",
    r"https://github.com/TanStack/table$": "https://tanstack.com/table/latest",
    r"https://github.com/TanStack/query$": "https://tanstack.com/query/latest",
    r"https://npmjs.com/package/@tanstack/react-table": "https://tanstack.com/table/latest",
    r"https://npmjs.com/package/react-table.*": "https://tanstack.com/table/latest",
    r"https://react-query-.*\.vercel\.app": "https://tanstack.com/query/latest",
    
    # MUI/Material-UI replacements
    r"https://v3\.mui\.com": "https://mui.com/material-ui/getting-started/installation/",
    r"https://npmjs.com/package/@material-ui/styles": "https://mui.com/material-ui/migration/v5-style-changes/",
    r"https://github.com/mui/material-ui": "https://mui.com/material-ui/",
    
    # Formik replacements
    r"https://github.com/jaredpalmer/formik/tree/[a-f0-9]+": "https://formik.org/docs/overview",
    r"https://github.com/jaredpalmer/formik/blob/main/docs/.*": "https://formik.org/docs/api/formik",
    r"https://github.com/jaredpalmer/formik$": "https://formik.org/docs/overview",
    
    # React Hook Form
    r"https://github.com/react-hook-form$": "https://react-hook-form.com/get-started",
    
    # Ant Design
    r"https://github.com/ant-design$": "https://ant.design/docs/react/introduce",
    r"https://github.com/ant-design/ant-design": "https://ant.design/docs/react/introduce",
    
    # Chakra UI
    r"https://github.com/chakra-ui/chakra-ui": "https://v2.chakra-ui.com/getting-started",
    r"https://v2\.chakra-ui\.com/getting-started/with-react-table": "https://v2.chakra-ui.com/docs/data-display/table",
    
    # React Use - keep master branch as it's still the default
    r"https://github.com/streamich/react-use/blob/HEAD/docs/(.*)\.md": r"https://github.com/streamich/react-use/blob/master/docs/\1.md",
    r"https://github.com/streamich/react-use$": "https://github.com/streamich/react-use",
    
    # Microsoft Fluent UI
    r"https://github.com/microsoft/fluentui/tree/[a-f0-9]+": "https://fluent2.microsoft.design/",
    r"https://github.com/microsoft/fluentui/tree/@fluentui/.*": "https://fluent2.microsoft.design/",
    r"https://github.com/microsoft/fluentui/tree/master/.*": "https://fluent2.microsoft.design/",
    r"https://github.com/microsoft/fluentui/compare/.*": "https://fluent2.microsoft.design/",
    r"https://github.com/microsoft/fluentui/wiki/.*": "https://fluent2.microsoft.design/",
    r"https://github.com/microsoft/fluentui$": "https://fluent2.microsoft.design/",
    r"https://github.com/OfficeDev/office-ui-fabric-react": "https://fluent2.microsoft.design/",
    r"https://npmjs.com/package/@fluentui/.*": "https://fluent2.microsoft.design/",
    r"https://fluent2\.microsoft\.design/components/web/react": "https://fluent2.microsoft.design/",
    
    # TypeScript
    r"https://github.com/microsoft/TypeScript/.*": "https://www.typescriptlang.org/docs/",
    r"https://typescriptlang.org/docs/handbook": "https://www.typescriptlang.org/docs/handbook/intro.html",
    
    # Other libraries with proper docs
    r"https://github.com/vercel/swr": "https://swr.vercel.app",
    r"https://swr\.bootcss\.com": "https://swr.vercel.app",
    r"https://github.com/vercel/next\.js": "https://nextjs.org/docs",
    r"https://github.com/remix-run/remix.*": "https://remix.run/docs/en/main",
    r"https://remix\.run/docs/en/1\.19\.3": "https://remix.run/docs/en/main",
    r"https://github.com/apollographql/apollo-client": "https://www.apollographql.com/docs/react/",
    r"https://github.com/angular/angular": "https://angular.dev/",
    r"https://github.com/solidjs/solid": "https://www.solidjs.com/docs/latest",
    r"https://start\.solidjs\.com": "https://www.solidjs.com/docs/latest",
    r"https://github.com/lit/lit.*": "https://lit.dev/docs/",
    r"https://github.com/aurelia/aurelia": "https://aurelia.io/docs",
    r"https://aurelia\.io/home": "https://aurelia.io/docs",
    r"https://github.com/nestjs.*": "https://docs.nestjs.com",
    r"https://github.com/nest-modules": "https://docs.nestjs.com",
    r"https://github.com/MichalLytek/type-graphql": "https://typegraphql.com/docs/introduction.html",
    r"https://github.com/web3/web3\.js": "https://web3js.readthedocs.io/",
    r"https://github.com/discordjs": "https://discord.js.org/docs",
    r"https://github.com/umijs/umi": "https://umijs.org/docs/introduce/introduce",
    r"https://github.com/denoland/deno": "https://docs.deno.com",
    r"https://github.com/storybookjs/storybook.*": "https://storybook.js.org/docs",
    r"https://storybook\.js\.org/showcase/.*": "https://storybook.js.org/docs",
    
    # InversifyJS
    r"https://github.com/lukas-zech-software/InversifyJS": "https://inversify.io/",
    r"https://github.com/inversify$": "https://inversify.io/",
    
    # Keep these as-is (already canonical)
    r"https://axios-http\.com": "https://axios-http.com/docs/intro",
    r"https://rxjs\.dev": "https://rxjs.dev/guide/overview",
    r"https://reactrouter\.com": "https://reactrouter.com/en/main",
    r"https://definitelytyped\.org": "https://definitelytyped.org/",
}

def clean_url(url):
    """Clean a single URL using the replacement rules."""
    for pattern, replacement in URL_REPLACEMENTS.items():
        if re.match(pattern, url):
            return re.sub(pattern, replacement, url)
    return url

def process_urls_file(input_file, output_file):
    """Process the urls-list.md file and create a cleaned version."""
    with open(input_file, 'r') as f:
        lines = f.readlines()
    
    cleaned_lines = []
    stats = {"updated": 0, "unchanged": 0}
    
    for line in lines:
        # Parse the JSON-like format
        match = re.match(r'{id:\s*(\d+),\s*url:\s*"([^"]+)"}', line.strip())
        if match:
            id_num = match.group(1)
            old_url = match.group(2)
            new_url = clean_url(old_url)
            
            if old_url != new_url:
                print(f"ID {id_num}: {old_url} -> {new_url}")
                stats["updated"] += 1
            else:
                stats["unchanged"] += 1
            
            cleaned_lines.append(f'{{id: {id_num}, url: "{new_url}"}}\n')
        else:
            cleaned_lines.append(line)
    
    with open(output_file, 'w') as f:
        f.writelines(cleaned_lines)
    
    print(f"\nSummary: {stats['updated']} URLs updated, {stats['unchanged']} unchanged")
    return stats

if __name__ == "__main__":
    input_file = "urls-list.md"
    output_file = "urls-list-cleaned.md"
    
    print("Cleaning URLs...")
    process_urls_file(input_file, output_file)
    print(f"\nCleaned URLs saved to {output_file}")