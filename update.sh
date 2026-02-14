#!/usr/bin/env bash

set -e

cd "$(dirname '$0')"

curl https://helldivers.wiki.gg/wiki/Stratagems > stratagems.html

source venv/bin/activate

cat > src/stratagems.rs << 'EOF'
use serde::{Deserialize, Serialize};

#[derive(Debug, Deserialize, Serialize)]
pub enum Binding {
    Up = 1,
    Down = 2,
    Left = 3,
    Right = 4,
}

#[derive(Debug, Deserialize, Serialize)]
pub struct Stratagem {
    name: String,
    binding: Vec<Binding>
}

impl Stratagem {
    pub fn binding(&self) -> &[Binding] {
        return &self.binding
    }

    pub fn name(&self) -> &str {
        return &self.name
    }

    pub fn new(name: String, binding: Vec<Binding>) -> Self {
        return Self { name, binding }
    }

    pub fn all_stratagems() -> Vec<Stratagem> {
        vec![
EOF

python web_parser.py >> src/stratagems.rs

cat >> src/stratagems.rs << 'EOF'
        ]
    }
}
EOF
