# Build Engine Specification Details

This document describes the general runtime contract for the build engine without enumerating verifier fixtures. The action_graph document is JSON with an edges collection and an actions collection. Each action has an identifier, a command string, and zero or more input paths; a target is the artifact path or action identifier that should appear as an active build output.

The engine stores graph and artifact state in SQLite through the sqlite3 driver. Consumers connect to the database, create a cursor, execute SQL statements, fetch one row or all rows as needed, and close the connection when done. The edges table uses from_node for the predecessor side of a dependency link and to_node for the dependent side. The artifacts table uses file_path as the active artifact key and stores the fingerprint value for that artifact. SQLite metadata such as total_changes and cursor rowcount may be observed but must not be required for correctness beyond normal database behavior.

The active manifest is a JSON mapping of artifact path to fingerprint. The engine may be invoked with explicit paths, but its defaults should match the documented in-container locations for the database, graph, and manifest. Test setup may remove directories with rmtree-style cleanup and recreate them with makedirs-style setup, so the engine must recreate required output directories and not depend on leftover files.

Go source inputs are fingerprinted from their public interface surface. Other input files are fingerprinted from their raw bytes. The verifier builds the Go source into the build_engine binary and checks observable behavior through the CLI, SQLite state, generated files, and manifest contents.
