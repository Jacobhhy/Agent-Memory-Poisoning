#!/usr/bin/env python3
"""
Run All MetaGPT Attack Experiments

This script runs all three attack experiments sequentially and generates
a comprehensive report.

Usage:
    python run_all_experiments.py [options]

Options:
    --skip-llm    Skip experiments that require LLM calls (exp1, exp2)
    --memory-only Run only memory-based experiments (exp3)
    --verbose     Enable verbose output
"""

import sys
import time
import argparse
from pathlib import Path
from datetime import datetime

# Add to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))


def print_banner():
    """Print ASCII banner."""
    banner = """
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║           MetaGPT Memory Poisoning Attack - Proof of Concept                 ║
║                                                                              ║
║  Three Novel Attack Primitives Against Memory-Based Agent Systems:          ║
║    1. Schema-Spoofing: External content → Internal reasoning                ║
║    2. JudgeJacking: Fake success markers → Validation bypass                ║
║    3. Memory Graft: Poisoned experiences → Persistent behavior drift        ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""
    print(banner)


def print_section(title: str):
    """Print formatted section header."""
    print("\n" + "=" * 80)
    print(f"  {title}")
    print("=" * 80 + "\n")


def run_experiment(exp_number: int, exp_name: str, exp_module: str) -> dict:
    """
    Run a single experiment and track results.
    
    Args:
        exp_number: Experiment number (1-3)
        exp_name: Human-readable experiment name
        exp_module: Python module path to experiment
        
    Returns:
        Dictionary with experiment results
    """
    print_section(f"EXPERIMENT {exp_number}: {exp_name}")
    
    start_time = time.time()
    success = False
    error = None
    
    try:
        print(f"Starting {exp_name}...")
        print()
        
        # Import and run the experiment
        if exp_number == 1:
            from experiments.exp1_schema_spoof import run_schema_spoof_experiment
            import asyncio
            asyncio.run(run_schema_spoof_experiment())
        elif exp_number == 2:
            from experiments.exp2_judge_jack import run_judgejack_experiment
            import asyncio
            asyncio.run(run_judgejack_experiment())
        elif exp_number == 3:
            from experiments.exp3_memory_graft import run_memory_graft_experiment
            import asyncio
            asyncio.run(run_memory_graft_experiment())
        
        success = True
        
    except KeyboardInterrupt:
        error = "Interrupted by user"
        print(f"\n⚠️  Experiment {exp_number} interrupted by user")
        
    except Exception as e:
        error = str(e)
        print(f"\n❌ Experiment {exp_number} failed: {e}")
        import traceback
        traceback.print_exc()
    
    end_time = time.time()
    duration = end_time - start_time
    
    result = {
        "number": exp_number,
        "name": exp_name,
        "success": success,
        "duration": duration,
        "error": error
    }
    
    print(f"\n{'✓' if success else '✗'} Experiment {exp_number} completed in {duration:.1f}s")
    
    return result


def generate_summary_report(results: list, output_file: Path):
    """Generate comprehensive summary report."""
    
    with open(output_file, 'w') as f:
        f.write("=" * 80 + "\n")
        f.write("METAGPT ATTACK POC - COMPREHENSIVE REPORT\n")
        f.write("=" * 80 + "\n\n")
        f.write(f"Timestamp: {datetime.now().isoformat()}\n")
        f.write(f"Total Experiments Run: {len(results)}\n\n")
        
        # Summary table
        f.write("EXPERIMENT SUMMARY\n")
        f.write("-" * 80 + "\n")
        f.write(f"{'#':<5} {'Experiment':<35} {'Status':<12} {'Duration':<12}\n")
        f.write("-" * 80 + "\n")
        
        total_duration = 0
        successful = 0
        
        for result in results:
            status = "✓ SUCCESS" if result["success"] else "✗ FAILED"
            duration_str = f"{result['duration']:.1f}s"
            
            f.write(f"{result['number']:<5} {result['name']:<35} {status:<12} {duration_str:<12}\n")
            
            if result["success"]:
                successful += 1
            total_duration += result["duration"]
        
        f.write("-" * 80 + "\n")
        f.write(f"Success Rate: {successful}/{len(results)} ({100*successful/len(results):.1f}%)\n")
        f.write(f"Total Runtime: {total_duration:.1f}s\n\n")
        
        # Detailed results
        f.write("DETAILED RESULTS\n")
        f.write("=" * 80 + "\n\n")
        
        for result in results:
            f.write(f"Experiment {result['number']}: {result['name']}\n")
            f.write("-" * 80 + "\n")
            f.write(f"Status: {'SUCCESS' if result['success'] else 'FAILED'}\n")
            f.write(f"Duration: {result['duration']:.1f}s\n")
            
            if result["error"]:
                f.write(f"Error: {result['error']}\n")
            
            f.write("\n")
        
        # Recommendations
        f.write("RECOMMENDATIONS\n")
        f.write("=" * 80 + "\n\n")
        
        if successful == len(results):
            f.write("✓ All experiments completed successfully!\n\n")
            f.write("Next steps:\n")
            f.write("  1. Review individual experiment results in results/ directory\n")
            f.write("  2. Analyze memory inspection and retrieval logs\n")
            f.write("  3. Consider implementing defenses against detected vulnerabilities\n")
            f.write("  4. Document findings for security team\n")
        else:
            f.write("⚠️  Some experiments failed or were incomplete.\n\n")
            f.write("Troubleshooting:\n")
            f.write("  1. Check error messages in this report\n")
            f.write("  2. Verify MetaGPT installation and configuration\n")
            f.write("  3. Ensure API keys are properly configured\n")
            f.write("  4. Review individual experiment logs\n")
        
        f.write("\n")
        f.write("=" * 80 + "\n")
        f.write("For detailed usage information, see USAGE.md\n")
        f.write("=" * 80 + "\n")


def main():
    """Main entry point."""
    
    parser = argparse.ArgumentParser(
        description="Run MetaGPT Attack POC experiments"
    )
    parser.add_argument(
        "--skip-llm",
        action="store_true",
        help="Skip experiments that require LLM API calls (exp1, exp2)"
    )
    parser.add_argument(
        "--memory-only",
        action="store_true",
        help="Run only memory-based experiments (exp3)"
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose output"
    )
    
    args = parser.parse_args()
    
    # Print banner
    print_banner()
    
    print("Starting MetaGPT Attack POC Experiments")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    if args.skip_llm or args.memory_only:
        print("⚠️  Running in limited mode:")
        if args.skip_llm:
            print("  • Skipping LLM-dependent experiments (exp1, exp2)")
        if args.memory_only:
            print("  • Running only memory experiments (exp3)")
        print()
    
    # Prepare results directory
    results_dir = Path(__file__).parent / "results"
    results_dir.mkdir(exist_ok=True)
    
    # Define experiments to run
    experiments = []
    
    if not (args.skip_llm or args.memory_only):
        experiments.append((1, "Schema-Spoofing Attack", "exp1_schema_spoof"))
        experiments.append((2, "JudgeJacking Attack", "exp2_judge_jack"))
    
    experiments.append((3, "Memory Graft Attack", "exp3_memory_graft"))
    
    print(f"Running {len(experiments)} experiment(s)...")
    print()
    
    # Run all experiments
    results = []
    
    for exp_num, exp_name, exp_module in experiments:
        result = run_experiment(exp_num, exp_name, exp_module)
        results.append(result)
        
        # Brief pause between experiments
        if exp_num < experiments[-1][0]:
            print("\nPreparing next experiment...\n")
            time.sleep(2)
    
    # Generate summary report
    print_section("GENERATING SUMMARY REPORT")
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    summary_file = results_dir / f"summary_report_{timestamp}.txt"
    
    generate_summary_report(results, summary_file)
    
    print(f"✓ Summary report generated: {summary_file}")
    print()
    
    # Print summary to console
    print_section("EXECUTION SUMMARY")
    
    successful = sum(1 for r in results if r["success"])
    total_duration = sum(r["duration"] for r in results)
    
    print(f"Experiments Run: {len(results)}")
    print(f"Successful: {successful}/{len(results)}")
    print(f"Total Runtime: {total_duration:.1f}s")
    print()
    
    for result in results:
        status = "✓" if result["success"] else "✗"
        print(f"  {status} Experiment {result['number']}: {result['name']}")
    
    print()
    print("=" * 80)
    print("All experiments complete!")
    print(f"Results saved to: {results_dir}")
    print(f"Summary report: {summary_file}")
    print("=" * 80)
    print()
    
    # Exit code
    if successful == len(results):
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Execution interrupted by user")
        sys.exit(130)
    except Exception as e:
        print(f"\n\n❌ Fatal error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
