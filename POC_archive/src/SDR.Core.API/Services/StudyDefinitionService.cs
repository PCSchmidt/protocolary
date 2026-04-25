using Microsoft.Extensions.Configuration;
using MongoDB.Driver;
using SDR.Core.API.Models;
using System;
using System.Collections.Generic;
using System.Threading.Tasks;

namespace SDR.Core.API.Services
{
    public class StudyDefinitionService : IStudyDefinitionService
    {
        private readonly IMongoCollection<StudyDefinition> _studyDefinitions;

        public StudyDefinitionService(IConfiguration configuration)
        {
            var client = new MongoClient(configuration.GetConnectionString("MongoDB"));
            var database = client.GetDatabase(configuration["Database:DatabaseName"]);
            _studyDefinitions = database.GetCollection<StudyDefinition>(configuration["Database:StudyDefinitionsContainer"]);
        }

        public async Task<IEnumerable<StudyDefinition>> GetAllAsync()
        {
            return await _studyDefinitions.Find(sd => true).ToListAsync();
        }

        public async Task<StudyDefinition> GetByIdAsync(string id)
        {
            return await _studyDefinitions.Find(sd => sd.Id == id).FirstOrDefaultAsync();
        }

        public async Task<StudyDefinition> CreateAsync(StudyDefinition studyDefinition)
        {
            if (string.IsNullOrEmpty(studyDefinition.Id))
            {
                studyDefinition.Id = Guid.NewGuid().ToString();
            }

            await _studyDefinitions.InsertOneAsync(studyDefinition);
            return studyDefinition;
        }

        public async Task UpdateAsync(StudyDefinition studyDefinition)
        {
            await _studyDefinitions.ReplaceOneAsync(sd => sd.Id == studyDefinition.Id, studyDefinition);
        }

        public async Task DeleteAsync(string id)
        {
            await _studyDefinitions.DeleteOneAsync(sd => sd.Id == id);
        }
    }
}
