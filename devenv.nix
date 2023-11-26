{ pkgs, ... }:

{
  dotenv.enable = true;

  packages = with pkgs; [
    git
    (ollama.override {
      llama-cpp = (llama-cpp.override {
        cudaSupport = true;
        openblasSupport = false;
      });
    })
    (python310.withPackages (p: [
      p.aiohttp
      p.aiomqtt
      p.beautifulsoup4
      p.fastapi
      p.langchain
      p.openai
      p.pytz
      p.rich
      p.typer
      p.uvicorn
    ]))
  ];
}
