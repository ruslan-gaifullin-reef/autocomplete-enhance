#!/usr/bin/env python
# PYTHON_ARGCOMPLETE_OK

import ast
import os
import sys


# from target_script import args

def load_ast(target='sample_cli/describe_github_user.py'):
    current_dir = os.path.dirname(__file__)
    script_path = os.path.join(current_dir, target)

    # Load the source code
    with open(script_path) as f:
        tree = ast.parse(f.read())
    return tree


def get_args(tree):
    # Identify the 'args' assignment node
    target_node = None
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(
                isinstance(t, ast.Name) and t.id == "args" for t in node.targets
        ):
            target_node = node
            break
    return target_node


def collect_dependencies(tree, target_node):
    # Collect dependencies for the target node
    class NameCollector(ast.NodeVisitor):
        def __init__(self):
            self.names = set()

        def visit_Name(self, node):
            self.names.add(node.id)

    # Initialize dependency set from the target value
    collector = NameCollector()
    collector.visit(target_node.value)
    deps = set(collector.names)
    # Ensure 'parser' is included if used
    deps.add('parser')

    dep_nodes = []
    changed = True
    while changed:
        changed = False
        for node in tree.body:
            # Include assignments that define a needed dependency
            if isinstance(node, ast.Assign):
                for t in node.targets:
                    if isinstance(t, ast.Name) and t.id in deps and node not in dep_nodes:
                        dep_nodes.append(node)
                        # Add new names from this assignment
                        new_collector = NameCollector()
                        new_collector.visit(node.value)
                        new_names = new_collector.names - deps
                        if new_names:
                            deps.update(new_names)
                            changed = True
            # Include attribute calls (e.g., parser.add_argument, argcomplete.autocomplete)
            if isinstance(node, ast.Expr) and isinstance(node.value, ast.Call):
                func = node.value.func
                if (
                        isinstance(func, ast.Attribute)
                        and isinstance(func.value, ast.Name)
                        and func.value.id in deps.union({'argcomplete'})
                ) and node not in dep_nodes:
                    dep_nodes.append(node)
                    changed = True
    return dep_nodes


def build_minimal_ast(tree, target_node, dep_nodes):
    # Build a minimal AST module: only argparse and argcomplete imports, necessary nodes, and the target assignment
    minimal_body = []
    for node in tree.body:
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            for alias in getattr(node, 'names', []):
                if alias.name in ('argparse', 'argcomplete'):
                    minimal_body.append(node)
                    break
    # Add dependency nodes and the target assignment
    minimal_body.extend(dep_nodes)
    minimal_body.append(target_node)

    # Add sys.argv override to preserve passed-in arguments
    argv_override = ast.parse("import sys; sys.argv = " + repr(sys.argv)).body
    minimal_body.extend(argv_override)
    # Add dependency nodes and the target assignment
    minimal_body.extend(dep_nodes)
    minimal_body.append(target_node)

    minimal_tree = ast.Module(body=minimal_body, type_ignores=[])

    return minimal_tree


def main():
    # Load the AST from the target script
    tree = load_ast()

    # Get the 'args' assignment node
    target_node = get_args(tree)

    # Collect dependencies for the target node
    dep_nodes = collect_dependencies(tree, target_node)

    # Build a minimal AST module
    minimal_tree = build_minimal_ast(tree, target_node, dep_nodes)

    # Execute in a clean namespace
    namespace = {}
    exec(compile(minimal_tree, filename="<ast>", mode="exec"), namespace)
    print(minimal_tree)
    # Execute in a clean namespace
    namespace = {}
    exec(compile(minimal_tree, filename="<ast>", mode="exec"), namespace)

    # Output the extracted variable
    print(namespace["args"])
    print('done')


if __name__ == "__main__":
    main()
