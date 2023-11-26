{ pkgs, ... }:

{
  packages = with pkgs; [
    git
    (python310.withPackages (p: [
      p.fastapi
      p.langchain
      p.openai
      p.rich
      p.typer
      p.uvicorn
    ]))
  ];
}
