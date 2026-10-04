{
  description = "environment setup";
  inputs.nixpkgs.url = "github:nixos/nixpkgs/02f754064dce1a8c2b4b301f25c43b44fe2bbfd";
  outputs = { self, nixpkgs }:
  let system = "x86_64-linux";
      pkgs = import nixpkgs { inherit system; };
  in {
    devShells.${system}.default = pkgs.mkShell {
      buildInputs = with pkgs; [
        (python314.withPackages (ps: with ps; [
          numpy
          pandas
          scikit-learn
          matplotlib
          seaborn
          notebook
        ]))
      ];
    };
  };
}
