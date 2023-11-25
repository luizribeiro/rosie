{ pkgs, ... }:

{
  packages = with pkgs; [
    git
    (python310.withPackages (p: [
      p.langchain
      p.openai
      p.rich
      p.typer
    ]))
  ];
}
